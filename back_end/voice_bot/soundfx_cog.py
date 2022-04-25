import asyncio
import os

import discord
from discord.ext import commands

from configs import CONFIGS


class VoiceError(Exception):
    pass


class SoundFXSource(discord.PCMVolumeTransformer):
    @staticmethod
    async def create_source(ctx: commands.Context, effect_id: str):
        # Convert effect_id into file location
        if not effect_id in CONFIGS.soundfx:
            raise VoiceError(f"Effect not found: {effect_id}")
        file_location = CONFIGS.soundfx[effect_id]
        abs_path = os.path.abspath(os.path.dirname(__file__))
        return discord.FFmpegPCMAudio(
            source=f"{abs_path}/{CONFIGS.soundfx_directory}/{file_location}"
        )


class VoiceState:
    def __init__(self, bot: commands.Bot, cog: commands.Cog, ctx: commands.Context):
        self.bot = bot
        self.cog = cog
        self.ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.effects = asyncio.Queue()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    async def get_new_current(self):
        self.current = await self.effects.get()

    async def audio_player_task(self):
        while True:
            self.next.clear()
            await self.get_new_current()
            self.voice.play(self.current, after=self.play_next_effect)
            await self.next.wait()

    def play_next_effect(self, error=None):
        if error:
            raise VoiceError(str(error))
        self.next.set()

    async def disconnect(self):
        await self.ctx.invoke(self.cog._leave)


class SoundFX(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, self, ctx)
            self.voice_states[ctx.guild.id] = state
        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage("This command can't be used in DM channels.")
        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send(f"An error occurred: {str(error)}")

    @commands.command(name="join", aliases=["summon"], invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):
        """Joins a voice channel."""
        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return
        ctx.voice_state.voice = await destination.connect()

    @commands.command(name="disconnect", aliases=["dc", "leave", "dis"])
    async def _leave(self, ctx: commands.Context, silent: bool = False):
        """Clears the queue and leaves the voice channel."""
        if not ctx.voice_state.voice:
            if not silent:
                await ctx.send("Not connected to any voice channel.")
            return
        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

    @commands.command(name="play", aliases=["p"])
    async def _play(self, ctx: commands.Context, effect_id: str):
        """Plays a sound effect"""
        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)
        async with ctx.typing():
            source = await SoundFXSource.create_source(ctx, effect_id, loop=self.bot.loop)
            await ctx.voice_state.effects.put(source)

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError("You are not connected to any voice channel.")
        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError("Bot is already in a voice channel.")

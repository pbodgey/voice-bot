"""The main module of the bot.

Written by Aaron Barge
Copyright 2022

Module for any intializations needed for the discord bot.
Permissions:
    Voice:
        Connect
        Speak
        Use Voice Activity
    General:
        Manage Channels
        Manage Webhooks
Permission Integer: 573571088
"""

from discord.ext import commands

from configs import CONFIGS
from soundfx_cog import SoundFX

bot = commands.Bot(command_prefix=CONFIGS.command_prefix, case_insensitive=CONFIGS.case_insensitive)

bot.add_cog(SoundFX(bot))

if __name__ == "__main__":
    bot.run(CONFIGS.token)

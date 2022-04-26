import * as configs from './../configs.json' assert { type: 'json' };
import * as ENV from './env.js';

function webhook_send(msg) {
    var request = new XMLHttpRequest();
    request.open("POST", ENV.ENV.WEBHOOK_URL);
    request.setRequestHeader('Content-type', 'application/json');
    const parms = {
        username: "SoundFX Bot",
        avatar_url: "",
        content: msg
    };
    request.send(JSON.stringify(parms));
};

export function join() {
    console.log(configs);
    webhook_send(configs.default.command_prefix + "join");
};

export function leave() {
    webhook_send(configs.default.command_prefix + "leave");
};

export function play(effect) {
    webhook_send(configs.default.command_prefix + "play " + effect);
};

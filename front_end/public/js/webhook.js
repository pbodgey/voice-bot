require('dotenv').config();
const configs = require("./../../configs.json");

webhook_send = function(msg) {
    var request = new XMLHttpRequest();
    request.open("POST", process.env.WEBHOOK_URL);
    request.setRequestHeader('Content-type', 'application/json');
    const parms = {
        username: "SoundFX Bot",
        avatar_url: "",
        content: msg
    };
    request.send(JSON.stringify(parms));
};

module.exports = {
    join: function() {
        webhook_send(configs.command_prefix + "join");
    },

    leave: function() {
        webhook_send(configs.command_prefix + "leave");
    },

    play: function(effect) {
        webhook_send(configs.command_prefix + "play " + effect);
    }
};
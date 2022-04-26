import * as webhook from './webhook.js';

document.addEventListener("DOMContentLoaded", function() {
    var join = document.getElementById('join');
    join.addEventListener('click', webhook.join);
});
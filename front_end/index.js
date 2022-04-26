const express = require('express');
const path = require('path');

var app = express();

app.use(express.static(path.join(__dirname, 'public')));

app.get('/', function (request, response) {
    response.sendFile(path.join(__dirname, 'public/html/index.html'));
});

var server = app.listen(5000, function() {
    console.log('Node server is running...');
});

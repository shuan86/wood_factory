const express = require('express');
const path = require('path');
const { createServer } = require('http');
const WebSocket = require('ws');

const app = express();

const server = createServer(app);
const wss = new WebSocket.Server({ server });

wss.on('connection', function (ws) {
    console.log("client joined.");

    // send "hello world" every 1 second.
    //var id = setInterval(() => ws.send("hello world!"), 100);

    ws.on('message', function (data) {
        console.log("client sent a message:", data);
        // ws.send(data)
        wss.clients.forEach(function each(client) {
            if (client !== ws && client.readyState === WebSocket.OPEN) {
                client.send(data);
            }
        });
    });

    ws.on('close', function () {
        console.log("client left.");
        // clearInterval(id);
    });
});

server.listen(12345, function () {
    console.log('Listening on http://localhost:12345');
});
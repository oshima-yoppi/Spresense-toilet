var http = require('http');
var fs = require('fs');
var url = require('url');
var WebSocket = require('ws');

const hostname = '10.204.47.155';
const PORT = 3000;

let a = "loading...";

// Create an HTTP server
var server = http.createServer(function (req, res) {
    if (req.url === '/' && req.method === 'GET') {
        fs.readFile('index.html', 'utf8', function (err, content) {
            if (err) {
                res.statusCode = 500;
                res.end('Internal Server Error');
            } else {
                res.writeHead(200, { 'Content-Type': 'text/html' });

                if (wsServer.clients.size > 0) {
                    // If there are connected WebSocket clients, send data to them
                    wsServer.clients.forEach(function each(client) {
                        client.send(a);
                    });
                }

                // Replace the placeholder with the current value of 'a'
                content = content.replace('<span id="data_placeholder"></span>', a);
                res.end(content);
            }
        });
    } else if (req.url === '/postData' && req.method === 'POST') {
        let data = '';
        req.on('data', function (chunk) {
            data += chunk;
        });

        req.on('end', function () {
            // Parse the query
            let postData = new URLSearchParams(data);
            for (const [key, value] of postData) {
                // Check the key
                if (key === 'data') {
                    console.log('POST data:', value);
                    a = determineStatus(value);
                    // Send the updated value to connected WebSocket clients
                    wsServer.clients.forEach(function each(client) {
                        client.send(a);
                    });
                    res.end(value);
                }
            }
        });
    } else {
        res.statusCode = 404;
        res.end('NotFound');
    }
});

// Create a WebSocket server
const wsServer = new WebSocket.Server({ noServer: true });

// Handle WebSocket connection
wsServer.on('connection', function connection(ws) {
    console.log('WebSocket connected');

    // Send the initial value to the connected WebSocket client
    ws.send(a);

    ws.on('close', function () {
        console.log('WebSocket disconnected');
    });
});

// Upgrade the HTTP server to support WebSocket
server.on('upgrade', function upgrade(request, socket, head) {
    wsServer.handleUpgrade(request, socket, head, function done(ws) {
        wsServer.emit('connection', ws, request);
    });
});

// Listen on port 3000
server.listen(PORT, () => {
    console.log(`Server running at http://${hostname}:${PORT}/`);
});

// Function to determine the status based on the received value
function determineStatus(value) {
    switch (value) {
        case '0':
            return '非常に空いています';
        case '1':
            return '空いています';
        case '2':
            return '混雑しています';
        case '3':
            return '非常に混雑しています';
        default:
            return 'loading...';
    }
}

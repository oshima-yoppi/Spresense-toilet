// サーバのコード

const http = require('http');
const fs = require('fs');
const WebSocket = require('ws');

const hostname = '10.204.47.155';
const PORT = 3000;

let a = "loading...";

// Create an HTTP server
const server = http.createServer((req, res) => {
    if (req.url === '/' && req.method === 'GET') {
        fs.readFile('index.html', 'utf8', (err, content) => {
            if (err) {
                res.statusCode = 500;
                res.end('Internal Server Error');
            } else {
                res.writeHead(200, { 'Content-Type': 'text/html' });
                // Replace the placeholder with the current value of 'a'
                content = content.replace('<span id="data_placeholder"></span>', a);
                res.end(content);
            }
        });
    } else if (req.url === '/postData' && req.method === 'POST') {
        let data = '';
        req.on('data', (chunk) => {
            data += chunk;
        });

        req.on('end', () => {
            const postData = new URLSearchParams(data);
            for (const [key, value] of postData) {
                if (key === 'data') {
                    console.log('POST data:', value);
                    a = determineStatus(value);
                    // Send the updated value to connected WebSocket clients
                    wsServer.clients.forEach((client) => {
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
wsServer.on('connection', (ws) => {
    console.log('WebSocket connected');

    // Send the initial value to the connected WebSocket client
    ws.send(a);

    ws.on('close', () => {
        console.log('WebSocket disconnected');
    });
});

// Upgrade the HTTP server to support WebSocket
server.on('upgrade', (request, socket, head) => {
    wsServer.handleUpgrade(request, socket, head, (ws) => {
        wsServer.emit('connection', ws, request);
    });
});

// Listen on port 3000
server.listen(PORT, hostname, () => {
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

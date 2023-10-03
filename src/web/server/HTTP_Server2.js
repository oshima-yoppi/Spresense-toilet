var http = require('http');
var fs = require('fs');
var querystring = require('querystring');
var url = require('url');
var WebSocket = require('ws');

var data;
var postData = {};
let a = 'loading...';
var displayValue = 'loading...';

// const hostname = '10.204.47.155';
const hostname = '172.17.254.13'
const PORT = 3000;

var server = http.createServer(function (req, res) {
    if (req.url === '/' && req.method === 'GET') {
        fs.readFile('index.html', 'utf8', function (err, content) {
            if (err) {
                res.statusCode = 500;
                res.end('Internal Server Error');
            } else {
                res.writeHead(200, { 'Content-Type': 'text/html' });

                if ('data' in postData && postData['data'].trim() !== '') {
                    console.log('GET Response :', displayValue);
                    content = content.replace('<span id="data_placeholder"></span>', displayValue);
                } else {
                    content = content.replace('<span id="data_placeholder"></span>', ' loading...');
                }
                res.end(content);
            }
        });

    } else if (req.url === '/postData' && req.method === 'POST') {
        data = '';
        req.on('data', function (chunk) {
            data += chunk;
        });

        req.on('end', function () {
            postData = querystring.parse(data);
            for (key in postData) {
                if (key == 'data') {
                    console.log('POST data    :', postData[key]);
                    res.end(postData[key]);
                    // Broadcast the updated data to all connected clients
                    wss.clients.forEach(function (client) {
                        if (client.readyState === WebSocket.OPEN) {
                            var value = postData['data'];
                            // console.log('GET Response :', value);

                            if (Math.floor(parseInt(value)%10) === 0){
                                id = 1;
                            }else if (Math.floor(parseInt(value)%10) === 1){
                                id = 2;
                            }else if (Math.floor(parseInt(value)%10) === 2){
                                id = 3;
                            }else{
                                id = 4;
                            }

                            if (Math.floor(parseInt(value)/10) === 0) {
                                displayValue = id + '非常に空いています';
                            } else if (Math.floor(parseInt(value)/10) === 1) {
                                displayValue = id + '空いています';
                            } else if (Math.floor(parseInt(value)/10) === 2) {
                                displayValue = id + '混雑しています';
                            } else if (Math.floor(parseInt(value)/10) === 3) {
                                displayValue = id + '非常に混雑しています';
                            } else {
                                displayValue = a;
                            }
                            client.send(displayValue);

                            
                            
                        }
                    });
                }
            }
        });
        
    } else {
        res.statusCode = 404;
        res.end('NotFound');
    }
});

var wss = new WebSocket.Server({ server });

wss.on('connection', function (ws) {
    // Send initial data to the connected client
    ws.send(a);
});

server.listen(PORT, () => {
    console.log(`Server running at http://${hostname}:${PORT}/`);
});

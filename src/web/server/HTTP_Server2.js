var http = require('http');
var fs = require('fs');
var querystring = require('querystring');
var url = require('url');
var data;
var postData = {};
const hostname = 'localhost';
const PORT = 3000;
let a = "loading..."

var server = http.createServer(function(req, res) {
    // Access '/', response back with the latest postData
    if (req.url === '/' && req.method === 'GET') {
        fs.readFile('index.html', 'utf8', function(err, content) {
            if (err) {
                res.statusCode = 500;
                res.end('Internal Server Error');
            } else {
                res.writeHead(200, { 'Content-Type': 'text/html' });

                if ('data' in postData && postData['data'].trim() !== '') {
                    // Embed postData['data'] into the HTML response
                    console.log("postData['data']:", postData['data'])
                    switch (postData['data']) {
                        
                        case '0':
                            console.log("選択された値: 0")
                            a = '非常に空いています';
                            break;

                        case '1':
                            console.log("選択された値: 1")
                            a = '空いています';
                            break;

                        case '2':
                            console.log("選択された値: 2")
                            a = '混雑しています';
                            break;

                        case '3':
                            console.log("選択された値: 3")
                            a = '非常に混雑しています';
                            break;

                        default:
                            a = "loading..."
                            console.log("error")
                    }
                    content = content.replace('<span id="data_placeholder"></span>', a);
                } else {
                    // If 'data' is empty, display "loading"
                    content = content.replace('<span id="data_placeholder"></span>', ' loading...');
                }
                res.end(content);
            }
        });
    } else if (req.url === '/postData' && req.method === 'POST') {
        data = '';
        req.on('data', function(chunk) {
            data += chunk;
        });

        req.on('end', function() {
            // Parse the query
            postData = querystring.parse(data);
            for (key in postData) {
                // check the key
                if (key == 'data') {
                    console.log('POST data    :', postData[key]);
                    res.end(postData[key]);
                }
            }
        });
    } else {
        res.statusCode = 404;
        res.end('NotFound');
    }
});

// Listen port 3000
server.listen(PORT, () => {
    console.log(`Server running at http://${hostname}:${PORT}/`);
});

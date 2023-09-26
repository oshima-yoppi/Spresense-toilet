var http = require('http');
var fs = require('fs');
var querystring = require('querystring');
var url = require('url');
var data;
var postData = {};
const hostname = '10.204.47.155';
const PORT = 3000;


var server = http.createServer(function(req, res) {
    if (req.url === '/' && req.method === 'GET') {
        // ファイルを読み込んでクライアントに送信
        fs.readFile('index.html', 'utf8', function(err, htmlContent) {
            if (err) {
                res.statusCode = 500;
                res.end('Internal Server Error');
            } else {
                res.setHeader('Content-Type', 'text/html');
                res.end(htmlContent);
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
                    res.setHeader('Content-Type', 'text/html');
                    // 以下の行でpostData['data']の値をHTMLページに表示
                    res.end(`POST Data: ${postData[key]}`);
                }
            }
        });
    }
    else {
	res.statusCode = 404;
	res.end('NotFound');
    }
});

// Listen port 10080
server.listen(PORT, () => {
    console.log(`Server running at http://${hostname}:${PORT}/`);
  });
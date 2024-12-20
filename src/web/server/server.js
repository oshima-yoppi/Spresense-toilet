var data;
var postData = {};
const hostname = '172.17.254.13';
// const hostname = '192.168.201.164'
const port = 3000;

var querystring = require('querystring');
const http = require("http");
var WebSocket = require('ws');
const getdata_fromclip = require('./getdata_fromclip');
const readFile = require('./readFile');


const server = http.createServer((request, response) => {
    if (request.url === "/" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "text/html"
        });
        readFile("view/index.html", response);

    } else if (request.url === "/index.html" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "text/html"
        });
        readFile("view/index.html", response);

    } else if (request.url === "/list_base.html" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "text/html"
        });
        readFile("view/list_base.html", response);

    } else if (request.url === "/list_building7.html" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "text/html"
        });
        readFile("view/list_building7.html", response);
       
    } else if (request.url === "/list_building12.html" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "text/html"
        });
        readFile("view/list_building12.html", response);

    } else if (request.url === "/list_building16.html" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "text/html"
        });
        readFile("view/list_building16.html", response);

    } else if (request.url === "/info.html" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "text/html"
        });
        readFile("view/info.html", response);

    } else if (request.url === "/faq.html" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "text/html"
        });
        readFile("view/faq.html", response);

    } else if (request.url === "/contact.html" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "text/html"
        });
        readFile("view/contact.html", response);

    } else if (request.url === "/privacy_policy.html" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "text/html"
        });
        readFile("view/privacy_policy.html", response);

    } else if (request.url === "/preparing.html" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "text/html"
        });
        readFile("view/preparing.html", response);

    } else if (request.url === "/public/images/ham.png" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "image/png"
        });
        readFile("public/images/ham.png", response);

    } else if (request.url === "/public/images/logo.png" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "image/png"
        });
        readFile("public/images/logo.png", response);

    } else if (request.url === "/public/images/toile1.png" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "image/png"
        });
        readFile("public/images/toile1.png", response);

    } else if (request.url === "/public/images/toile2.png" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "image/png"
        });
        readFile("public/images/toile2.png", response);

    } else if (request.url === "/public/images/toile3.png" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "image/png"
        });
        readFile("public/images/toile3.png", response);

    } else if (request.url === "/public/images/toile4.png" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "image/png"
        });
        readFile("public/images/toile4.png", response);

    } else if (request.url === "/public/images/building7.png" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "image/png"
        });
        readFile("public/images/building7.png", response);

    } else if (request.url === "/public/images/building12.png" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "image/png"
        });
        readFile("public/images/building12.png", response);

    } else if (request.url === "/public/images/building16.png" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "image/png"
        });
        readFile("public/images/building16.png", response);

    } else if (request.url === "/public/images/happy.png" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "image/png"
        });
        readFile("public/images/happy.png", response);

    } else if (request.url === "/public/images/arrow1.gif" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "image/gif"
        });
        readFile("public/images/arrow1.gif", response);

    } else if (request.url === "/public/css/style.css" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "text/css"
        });
        readFile("public/css/style.css", response);

    } else if (request.url === "/js/main.js" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "text/css"
        });
        readFile("view/js/main.js", response);

    } else if (request.url === "/js/slick.js" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "text/css"
        });
        readFile("view/js/slick.js", response);
    
    } else if (request.url === "/js/vegas.js" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "text/css"
        });
        readFile("view/js/vegas.js", response);
    } else if (request.url === "/js/update.js" && request.method === "GET") {
        response.writeHead(200, {
            "Content-Type": "text/css"
        });
        readFile("view/js/update.js", response);

    } else if (request.url === '/postData' && request.method === 'POST') {
        data = '';
        request.on('data', function (chunk) {
            data += chunk;
        });

        request.on('end', function () {
            postData = querystring.parse(data);
            for (key in postData) {
                if (key == 'data') {
                    // console.log('POST data    :', postData[key]);
                    response.end(postData[key]);
                    wss.clients.forEach(function (client) {
                        if (client.readyState === WebSocket.OPEN) {
                            var value = postData['data'];
                            client.send(value);
                        }
                    });
                }
            }
        });

    } else {
        response.statusCode = 404;
        response.end('NotFound');
    }
});

var wss = new WebSocket.Server({ server });

// wss.on('connection', function (ws) {
//     ws.send('loading...');
// });

wss.on('connection', (socket) => {
    // console.log('クライアントが接続しました');

    const sendInterval = setInterval(() => {
        if (socket.readyState === WebSocket.OPEN) {
            getdata_fromclip()
                .then((payloaddata) => {
                    socket.send(payloaddata);
                    console.log("eltres",payloaddata)
                })
                .catch((error) => {
                    console.error('Error in processData chain:', error);
                });
        }
    }, 60 * 1000);


    // クライアントが切断したときの処理
    socket.on('close', () => {
        // console.log('クライアントが切断しました');
        clearInterval(sendInterval);
    });
});

server.listen(port, () => {
    console.log(`Server running at http://${hostname}:${port}/`);
});
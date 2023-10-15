const fs = require("fs");

function readFile(file, response) {
    fs.readFile(`./${file}`, (errors, data) => {
        if (errors) {
            console.log("Error reading the file...");
        }
        response.end(data);
    });
}

module.exports = readFile;
var getdata_fromclip = function() {
  const { get } = require('http');
  const { exec } = require('child_process');
  var url = 'https://api.clip-viewer-lite.com/auth/token';
  const key = 'oy7yTZo5f39KL0TWEYIhw6tR198DTvZRjI0zZjTi';
  const username = 'oosima@kimura-lab.net';
  const password = 'GL9D48xbXUK6UU8';

  const curlCommand = `curl -X POST -H "X-API-Key: ${key}" -d "{\\"username\\": \\"${username}\\", \\"password\\": \\"${password}\\"}" "${url}"`;

  exec(curlCommand, (error, stdout, stderr) => {
    if (error) {
      console.error(`エラーが発生しました: ${error.message}`);
      return;
    }

    const token = JSON.parse(stdout).token;
    var url = 'https://api.clip-viewer-lite.com/payload/latest/00010197a7';
    const curlCommand2 = `curl -X GET -H "X-API-Key: ${key}" -H "Authorization: ${token}" "${url}"`;

    exec(curlCommand2, (error, stdout, stderr) => {
      if (error) {
        console.error(`エラーが発生しました: ${error.message}`);
        return;
      }
    });
  });
}

var a = getdata_fromclip();
console.log(a);
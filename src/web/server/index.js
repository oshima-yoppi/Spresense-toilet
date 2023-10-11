const { exec } = require('child_process');

var getdata_fromclip = function () {
  return new Promise((resolve, reject) => {
    const url = 'https://api.clip-viewer-lite.com/auth/token';
    const key = 'oy7yTZo5f39KL0TWEYIhw6tR198DTvZRjI0zZjTi';
    const username = 'oosima@kimura-lab.net';
    const password = 'GL9D48xbXUK6UU8';

    const curlCommand = `curl -X POST -H "X-API-Key: ${key}" -d "{\\"username\\": \\"${username}\\", \\"password\\": \\"${password}\\"}" "${url}"`;

    exec(curlCommand, (error, stdout, stderr) => {
      if (error) {
        console.error(`error: ${error.message}`);
        reject(error);
      }

      const token = JSON.parse(stdout).token;
      const url = 'https://api.clip-viewer-lite.com/payload/latest/00010197a7';
      const curlCommand = `curl -X GET -H "X-API-Key: ${key}" -H "Authorization: ${token}" "${url}"`;

      exec(curlCommand, (error, stdout, stderr) => {
        if (error) {
          console.error(`error: ${error.message}`);
          reject(error);
        }
        var payloaddata = JSON.parse(stdout).payload[0].payload;
        payloaddata = payloaddata.slice(0,2);
        payloaddata = parseInt(payloaddata, 16)
        resolve(payloaddata);
      });
    });
  });
};

(async () => {
  try {
    const payloaddata = await getdata_fromclip();
    console.log(payloaddata);
  } catch (error) {
    console.error('error:', error);
  }
})();

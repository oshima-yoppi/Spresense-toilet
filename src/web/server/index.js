// var getdata_fromclip = function() {
//   const { exec } = require('child_process');
//   var url = 'https://api.clip-viewer-lite.com/auth/token';
//   const key = 'oy7yTZo5f39KL0TWEYIhw6tR198DTvZRjI0zZjTi';
//   const username = 'oosima@kimura-lab.net';
//   const password = 'GL9D48xbXUK6UU8';

//   const curlCommand = `curl -X POST -H "X-API-Key: ${key}" -d "{\\"username\\": \\"${username}\\", \\"password\\": \\"${password}\\"}" "${url}"`;

//   exec(curlCommand, (error, stdout, stderr) => {
//     if (error) {
//       console.error(`エラーが発生しました: ${error.message}`);
//       return -1;
//     }

//     const token = JSON.parse(stdout).token;
//     var url = 'https://api.clip-viewer-lite.com/payload/latest/00010197a7';
//     const curlCommand2 = `curl -X GET -H "X-API-Key: ${key}" -H "Authorization: ${token}" "${url}"`;

//     exec(curlCommand2, (error, stdout, stderr) => {
//       if (error) {
//         console.error(`エラーが発生しました: ${error.message}`);
//         return -1;
//       }
//       payloaddata = JSON.parse(stdout).payload[0].payload;
//       return payloaddata;
//     });
//   });
// }

// const a = getdata_fromclip();
// console.log(a);

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
        console.error(`エラーが発生しました: ${error.message}`);
        reject(error);
      }

      const token = JSON.parse(stdout).token;
      const url = 'https://api.clip-viewer-lite.com/payload/latest/00010197a7';
      const curlCommand2 = `curl -X GET -H "X-API-Key: ${key}" -H "Authorization: ${token}" "${url}"`;

      exec(curlCommand2, (error, stdout, stderr) => {
        if (error) {
          console.error(`エラーが発生しました: ${error.message}`);
          reject(error);
        }
        const payloaddata = JSON.parse(stdout).payload[0].payload;
        resolve(payloaddata);
      });
    });
  });
};

// 非同期処理を待つためにasync/awaitを使用
(async () => {
  try {
    const a = await getdata_fromclip();
    console.log("1",a);
  } catch (error) {
    console.error('処理中にエラーが発生しました:', error);
  }
})();

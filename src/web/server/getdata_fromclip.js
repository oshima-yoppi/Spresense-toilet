const util = require('util');
const { exec } = require('child_process');

const promisifiedExec = util.promisify(exec);

const getToken = async () => {
  const url = 'https://api.clip-viewer-lite.com/auth/token';
  const key = 'oy7yTZo5f39KL0TWEYIhw6tR198DTvZRjI0zZjTi';
  const username = 'oosima@kimura-lab.net';
  const password = 'GL9D48xbXUK6UU8';

  const curlCommand = `curl -X POST -H "X-API-Key: ${key}" -d "{\\"username\\": \\"${username}\\", \\"password\\": \\"${password}\\"}" "${url}"`;

  const { stdout, stderr } = await promisifiedExec(curlCommand);

  const token = JSON.parse(stdout).token;
  return token;
};

const getDataFromClip = async () => {
  try {
    const token = await getToken();

    const url = 'https://api.clip-viewer-lite.com/payload/latest/00010197a7';
    const key = 'oy7yTZo5f39KL0TWEYIhw6tR198DTvZRjI0zZjTi';
    const curlCommand = `curl -X GET -H "X-API-Key: ${key}" -H "Authorization: ${token}" "${url}"`;

    const { stdout, stderr } = await promisifiedExec(curlCommand);

    return stdout;
  } catch (error) {
    console.error(error); // エラーの内容を確認する
    throw error;
  }
};

const processData = async () => {
  try {
    var payloaddata = await getDataFromClip();
    const parseData = JSON.parse(payloaddata);

    if (parseData.result === 'success') {
      payloaddata = parseData.payload[0].payload.slice(0, 2);
      payloaddata = parseInt(payloaddata, 16);
    } else {
      payloaddata = 0;
    }

    return payloaddata;  // Promiseが解決する値を返す
  } catch (error) {
    console.error('Error in processData:', error);
    throw error;
  }
};

module.exports = processData;
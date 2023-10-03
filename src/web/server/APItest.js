const axios = require('axios');

// 送信先の外部サーバーのAPI URL
const externalApiUrl = "https://api.clip-viewer-lite.com/payload/latest/00010197a7";

// カスタムヘッダー
const customHeaders = {
  'X-API-Key': 'oy7yTZo5f39KL0TWEYIhw6tR198DTvZRjI0zZjTi',
  'Authorization': 'eyJraWQiOiJcL0FPakptYkJFQmszMFJkV0kzNFNoT1ErSk5NVGRsTEJSNzdxOWhmVjR2Zz0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyNmM3Mjg2NS00ZDM5LTQwYzgtOTYxNS05NWNlMGQ1Njg5NTAiLCJjb2duaXRvOmdyb3VwcyI6WyJNZW1iZXJzIl0sImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0yLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMl8zQUg2TEZpTUkiLCJjb2duaXRvOnVzZXJuYW1lIjoib29zaW1hQGtpbXVyYS1sYWIubmV0Iiwib3JpZ2luX2p0aSI6IjkzNjIxZmM5LWIyZWItNDViYi1hMmNiLTExNTQ4YWNhZWE5OCIsImF1ZCI6IjQzcGVyMTh2cThzZjMyMHI2MXVuYWRqNzh1IiwiZXZlbnRfaWQiOiJmMWRiNDFkYi1iZjk5LTQxODYtOTM3Yy1hNmI2MGFiYTFlOWEiLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTY5NjMwMDE3NCwiZXhwIjoxNjk2MzAwNDc0LCJpYXQiOjE2OTYzMDAxNzQsImp0aSI6IjljZTBhOWVlLWY2N2QtNDFiZC1iZjZhLTk3MDZiOWMwNDRmOCIsImVtYWlsIjoib29zaW1hQGtpbXVyYS1sYWIubmV0In0.wil1QpzxR4rWxlITBYfWDesGjRmqTuaMbgDWiA7vRx6GnPI2Irwj6zFsu-ECS8Q4WxF_mMfYYF4ddy0XM5qAvO3SRFWW1ZFzP_hfu0ifxgxAbUcIlSaV7GVzbX_ZjX2RtMgUSAZej9vSgx75bVVn28R3V8TfT-LRs5se5JkbrUGHpEptlt6WLKkDKbfzuYKOCguAQLd8aJ--hgL7COKL8oINREJJose-Soq53UUMD4OztiCSP16wJ2h-HqD_8puRQllJ2joIwtMziG1xIeTpYekZYoh3qFGO0jXvota87NNadhMVaN3HorXyNE4pZTv2__uUMbaIhFW7Wy5SrUk1ZA',
  // 他に必要なヘッダーがあれば追加
};

// axiosを使用してHTTP GETリクエストを送信
axios.get(externalApiUrl, {
  headers: customHeaders,
})
  .then(response => {
    console.log('HTTPリクエスト成功:', response.data);
  })
  .catch(error => {
    console.error('HTTPリクエストエラー:', error.message);
  });
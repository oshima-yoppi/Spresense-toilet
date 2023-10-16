const socket = new WebSocket('ws://172.17.254.13:3000');
let id = 0;
let data = 0;

function updateData(index, data) {
    if (index != 0){
    document.getElementById(`data_placeholder_${index}`).innerText = data;
    }
}

function CongestionJudgment(data){
    if (data == 0){
        return "非常に空いています";
    } else if (data <= 3) {
        return "空いています"; 
    } else if (data <= 5) {
        return "混雑しています";
    } else {
        return "非常に混雑しています";
    }

}

// 接続が開かれた時の処理
socket.addEventListener('open', (event) => {
    console.log('WebSocketに接続しました');
});

// メッセージを受信した時の処理
socket.addEventListener('message', (event) => {
    console.log('サーバーからのメッセージ:', event.data);

    // データをidとdataに加工
    id   = Math.floor(event.data/100);
    data = event.data%100;

    //NaNが含まれる場合の処理 --> 0にする
    if (isNaN(id) || isNaN(data)){
        id = 0;
        data = 0;
    }
    data = CongestionJudgment(data);
    // ここでデータを更新
    updateData(id, data);
});

// 接続が閉じられた時の処理
socket.addEventListener('close', (event) => {
    console.log('WebSocketの接続が閉じられました');
});
// const socket = new WebSocket('ws://172.17.254.13:3000'); //kimura-lab
const socket = new WebSocket('ws://192.168.27.164:3000'); //スマホ
let id = 0;
let data = 0;

function updateData(index, congestion, time, data) {
    if (index != 0){
    document.getElementById(`congestion_placeholder_${index}`).innerText = congestion;
    document.getElementById(`time_placeholder_${index}`).innerText = time+"分";
    document.getElementById(`table_time_placeholder_${index}`).innerText = time+"分";

    const emoji = "👤";
    const emojicontainer = document.getElementById(`people_placeholder_${index}`);
    emojicontainer.innerHTML = "";
    for (let i = 0; i < data; i++) {
        emojicontainer.innerHTML += emoji;
    }
    }
}

function CongestionJudgment(data){
    if (data == 0){
        return "非常に空いている";
    } else if (data <= 3) {
        return "空いている"; 
    } else if (data <= 5) {
        return "混雑している";
    } else {
        return "非常に混雑している";
    }
}

function WaitingtimeCalculation(data){
    ramda = 0.2;
    mu = 0.2;
    s = 4;
    rho = ramda/(mu*s);
    w = (1/mu)*(rho/(1-rho))*data;

    return w;
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
    time = Math.floor(WaitingtimeCalculation(data));
    congestion = CongestionJudgment(data);
    
    console.log(w);
    // ここでデータを更新
    updateData(id, congestion, time, data);
});

// 接続が閉じられた時の処理
socket.addEventListener('close', (event) => {
    console.log('WebSocketの接続が閉じられました');
});
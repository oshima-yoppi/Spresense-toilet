# トイレのクラウドモニター by spresense and MobileNetV2
 

 
spresense上でmobilenetを動かし、トイレの空き状況をクラウドに送信する

 
# DEMO
 
"hoge"の魅力が直感的に伝えわるデモ動画や図解を載せる
 
# Features
 
"hoge"のセールスポイントや差別化などを説明する
 
# Requirement
 
MobileNetを学習させるために、tensorflowをインストールする必要あり。
 
* tensorflow-gpu==2.8.0

またその他のライブラリもインストールする必要があります。アナコンダで環境を作成する場合は以下のコマンドを実行。
     
```bash
conda env create -f conda.yml
```

 
# ディレクトリの説明
## env
アナコンダの環境ファイルがまとまっています。
## src
ソースコードがまとまっています。
### AI
機械学習系のソースコードがまとまってます。このディレクトリにあるソースコードは自分のPC上で動かします。 
 - `train.py` ： MobileNetを学習させるためのコード
 - `gpu.py`：自分のPCでGPUが使えるかどうかを確認するためのコード
 - `test.py`：学習したモデルを使ってテストするためのコード
 - `make_dataset.py`：データセットを作成するためのコード
 - `view_dataset.py`：データセットの中身を確認するためのコード

### Spresense
Spresense上で実際に動かすコードです。
`ai_cam_lcd`に動かすやつが入ってる・

 
# Usage
 
DEMOの実行方法など、"hoge"の基本的な使い方を説明する
 
```bash
git clone https://github.com/hoge/~
cd examples
python demo.py
```
 
# Note
 
注意点などがあれば書く
 
# Author
 
作成情報を列挙する
 
* 作成者
* 所属
* E-mail
 
# License
ライセンスを明示する
 
"hoge" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
 
社内向けなら社外秘であることを明示してる
 
"hoge" is Confidential.
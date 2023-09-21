

 
# ディレクトリの説明
このディレクトリは主に、人検知のモデルを学習させるためのコードがまとまっています。このディレクトリにあるソースコードは自分のPC上で動かします。 
### ディレクトリ
 - `check_data`：データセットの中身を確認するための画像が保存される。
 - `imgs`：テストデータとして使う画像が保存される。
 - `models`：学習したモデルが保存される。
 - `module`：設定定数や、関数などが定義されている。
### ファイル
 - `train.py` ： MobileNetを学習させるためのコード
 - `gpu.py`：自分のPCでGPUが使えるかどうかを確認するためのコード
 - `test.py`：学習したモデルを使ってテストするためのコード
 - `make_dataset.py`：データセットを作成するためのコード
 - `view_dataset.py`：データセットの中身を確認するためのコード




# 使い方
## データセットのダウンロード
学習データとテスト用の画像をダウンロードします。
1. 学習データ  
[ここのドライブリンク](https://drive.google.com/drive/folders/1TG5E54d8ZgZTDf00AfXFOc9XzJVlTGZr?usp=drive_link)より、`imgs`フォルダをダウンロードし、このディレクトリに保存。

2. テスト用データ  
[ここのドライブリンク](https://drive.google.com/drive/folders/11jL48oYxZTncWYO84Qm-NZR4xx1J8uxO?usp=drive_link)より、`images.zip`をダウンロードする。そしたら、`annotations`フォルダと`images`フォルダと`classses.txt`ファイルが出てくると思います。次に、現在のディレクトリ配下に`rawdata`を作成し、それらを`rawdata`内に保存してください。

## 学習データの作成
`make_dataset.py`で、先ほどダウンロードした学習データセットを、tensroflowで学習しやすいように、データセットを作成します。
 

## 学習と検証
`train.py`で学習が開始されます。`test.py`で、`imgs`内のテスト用データを用いて学習されたモデルの検証を行います。
`test_tflite.py`では、量子化されたモデルでの検証を行います。
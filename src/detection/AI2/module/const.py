import os

INPUT_SIZE = (96, 96)
NUM_AREA = 12  # 12の約数にすること
LABEL_SIZE = (NUM_AREA, NUM_AREA)
INPUT_CHANNEL = 3
ALPHA = 0.75  # 1はダメ0.5は行ける
SPLIT_NUM = 1

RAW_DATA_DIR = "rawdata"  # 生データ
DATA_DIR = "data"  # データセット。生データを変換したもの

# 保存するモデルのパス
MODEL_DIR = "model"
SPRESENSE_MODEL_DIR = "../../Spresense/detect_people/"
FULL_MODEL_PATH = os.path.join(MODEL_DIR, "model.h5")
TFLITE_MODEL_PATH = os.path.join(MODEL_DIR, "model.tflite")
TFLITE_QUANT_MODEL_PATH = os.path.join(MODEL_DIR, "model_quant.tflite")
HEADER_MODEL_PATH = os.path.join(MODEL_DIR, "spresense_model.h")
HEADER_QUANT_MODEL_PATH = os.path.join(MODEL_DIR, "spresense_model_quant2.h")

SPRESENSE_HEADER_QUANT_MODEL_PATH = os.path.join(
    SPRESENSE_MODEL_DIR, "spresense_model_quant.h"
)
SPRESENSE_HEADER_MODEL_PATH = os.path.join(SPRESENSE_MODEL_DIR, "spresense_model.h")

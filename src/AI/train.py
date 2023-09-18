# %%

import tensorflow as tf
from keras.layers import (
    Dense,
    Input,
    GlobalAveragePooling2D,
    Dropout,
    BatchNormalization,
    UpSampling2D,
    Conv2D,
    MaxPooling2D,
    AveragePooling2D,
    Flatten,
    Concatenate,
)
from tensorflow.keras.optimizers import Adam
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import CSVLogger
from keras.models import Model
from tensorflow.keras.applications import MobileNet, MobileNetV2
from tensorflow import keras

# import tensorflow_model_optimization as tfmot
from keras import backend as K
from tqdm import tqdm
import os
import sys
import numpy as np
import h5py
import matplotlib.pyplot as plt
import cv2
from module.const import *
from module import func, loss
import random

# %%
# # データセット
x_train = []
y_train = []
x_test = []
y_test = []
x_valid = []
y_valid = []
ignore = False  # falseの方が精度が高い

trans_lst = []
center = (INPUT_SIZE[0] / 2, INPUT_SIZE[1] / 2)
scale = 1.0
for i in [theta for theta in range(0, 360, 30)]:
    trans_lst.append(cv2.getRotationMatrix2D(center, i, scale))

    # for dir in ["train", "valid"]:
dataset = []
for path in os.listdir(DATA_DIR):
    path = os.path.join(DATA_DIR, path)
    with h5py.File(path, "r") as f:
        img = f["img"][:]
        label = f["label"][:]
    dataset.append((img, label))
random_idx = list(range(0, len(dataset)))

# データをランダムに取得するためのインデックス
random.shuffle(random_idx)
# データ取得。データ数が少ないため、auguentationを行う。回転、反転、明るさ調整を行い、学習データに追加。
for i, idx in enumerate(tqdm(random_idx)):
    img, label = dataset[idx]
    if i < len(random_idx) * 0.9:
        for trans in trans_lst:
            img_trans = cv2.warpAffine(img, trans, INPUT_SIZE)
            label_trans = cv2.warpAffine(label, trans, INPUT_SIZE)
            img_trans = func.augment_brightness(img_trans)
            x_train.append(img_trans)
            y_train.append(func.label_change(label_trans, ignore_haji=ignore))
            img_trans = np.fliplr(img_trans)
            img_trans = func.augment_brightness(img_trans)
            x_train.append(img_trans)
            y_train.append(
                func.label_change(np.fliplr(label_trans), ignore_haji=ignore)
            )

    else:
        x_valid.append(img)
        y_valid.append(func.label_change(label, ignore_haji=ignore))
    # break

# print(f"x_train: {len(x_train)}, x_test: {len(x_test)}, x_valid: {len(x_valid)}")

# # データの正規化を行う
x_train = np.array(x_train) / 255
y_train = np.array(y_train)
x_test = np.array(x_test) / 255
y_test = np.array(y_test)
x_valid = np.array(x_valid) / 255
y_valid = np.array(y_valid)


# %%
"""
モデルの定義
"""

mobilenet = MobileNetV2(
    input_shape=(INPUT_SIZE[0], INPUT_SIZE[1], INPUT_CHANNEL),
    include_top=False,
    alpha=ALPHA,
    weights="imagenet"
)
mobilenet.summary()  
complessed_mobilenet = Model(
    inputs=mobilenet.input, outputs=mobilenet.get_layer("block_6_expand_relu").output
)
# for layer in mobilenet.layers:
#     print(layer.name)
# complessed_mobilenet = Model(
#     inputs=mobilenet.input, outputs=mobilenet.get_layer("re_lu_1").output
# )
for layer in complessed_mobilenet.layers:
    layer.trainable = False

# 出力をlabelsizeに合わせるための変数を定義。)
mobile_output = 12
padding_h = mobile_output % LABEL_SIZE[0]
padding_w = mobile_output % LABEL_SIZE[1]
stride_h = (mobile_output + padding_h * 2) // LABEL_SIZE[0]
stride_w = (mobile_output + padding_w * 2) // LABEL_SIZE[1]
pool_h = (mobile_output + padding_h * 2) // LABEL_SIZE[0]
pool_w = (mobile_output + padding_w * 2) // LABEL_SIZE[1]

# 自作のモデルを定義。mobilenet + Conv*3
custom_model = tf.keras.models.Sequential(
    [
        complessed_mobilenet,
        MaxPooling2D(
            pool_size=(pool_h, pool_w),
            strides=(stride_h, stride_w),
        ),  # max >> average 終盤に就けるより前の方がいい
        Conv2D(
            filters=32,
            kernel_size=1,
            strides=1,
            padding="same",
            activation="relu",
        ),
        tf.keras.layers.BatchNormalization(),
        Conv2D(
            filters=32,
            kernel_size=1,
            strides=1,
            padding="same",
            activation="relu",
        ),
        tf.keras.layers.BatchNormalization(),
        Conv2D(
            filters=1,
            kernel_size=1,
            strides=1,
            padding="same",
            activation="sigmoid",
        ),
    ]
)

custom_model.summary()
total_params = custom_model.count_params()
print("Total params: ", total_params)
print("Total RAM :", total_params * 4 / 1024 / 1024, "MB")  #


# %%

"""
学習を行う
"""

custom_model.compile(
    loss=loss.DiceLoss,
    optimizer=Adam(learning_rate=0.001),
    metrics=[loss.IoU],
)
custom_model.fit(
    x_train,
    y_train,
    batch_size=32,
    epochs=50,
    validation_data=(x_valid, y_valid),
)



# %%
"""
save Model
"""
if os.path.exists(MODEL_DIR) == False:
    os.mkdir(MODEL_DIR)

custom_model.save(FULL_MODEL_PATH)
conveter = tf.lite.TFLiteConverter.from_keras_model(custom_model)
tflite_model = conveter.convert()
float_model_size = len(tflite_model) / 1024 / 1024
print(f"float model size: {float_model_size} MB")
open(TFLITE_MODEL_PATH, "wb").write(tflite_model)


import binascii


def convert_to_c_array(bytes) -> str:
    hexstr = binascii.hexlify(bytes).decode("UTF-8")
    hexstr = hexstr.upper()
    array = ["0x" + hexstr[i : i + 2] for i in range(0, len(hexstr), 2)]
    array = [array[i : i + 10] for i in range(0, len(array), 10)]
    return ",\n  ".join([", ".join(e) for e in array])


tflite_binary = open(TFLITE_MODEL_PATH, "rb").read()
ascii_bytes = convert_to_c_array(tflite_binary)
header_file = (
    "const unsigned char model_tflite[] = {\n  "
    + ascii_bytes
    + "\n};\nunsigned int model_tflite_len = "
    + str(len(tflite_binary))
    + ";"
)
# print(c_file)
open(HEADER_MODEL_PATH, "w").write(header_file)
open(SPRESENSE_HEADER_MODEL_PATH, "w").write(header_file)
#%%
print('--------start quantization--------')

def representative_dataset_gen():
   for i in range(len(x_valid)):
      input_image = tf.cast(x_valid[i], tf.float32)
      input_image = tf.reshape(input_image, [1,INPUT_SIZE[0],INPUT_SIZE[1],INPUT_CHANNEL])
      yield ([input_image])


converter = tf.lite.TFLiteConverter.from_keras_model(custom_model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_dataset_gen
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
# converter.inference_input_type = tf.int8
# converter.inference_output_type = tf.int8
tflite_quant_model = converter.convert()

tflite_quant_model_path = os.path.join(MODEL_DIR, "model_quant.tflite")
with open(tflite_quant_model_path, 'wb') as f:
   f.write(tflite_quant_model)
spresense_quant_model_path = os.path.join(MODEL_DIR, "spresense_model_quant.h")
tflite_binary = open(tflite_quant_model_path, "rb").read()
ascii_bytes = convert_to_c_array(tflite_binary)
header_file = (
    "const unsigned char model_tflite[] = {\n  "
    + ascii_bytes
    + "\n};\nunsigned int model_tflite_len = "
    + str(len(tflite_binary))
    + ";"
)

open(HEADER_QUANT_MODEL_PATH, "w").write(header_file)
open(SPRESENSE_HEADER_QUANT_MODEL_PATH, "w").write(header_file)
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


def set_seed(seed=42):
    tf.random.set_seed(seed)
    np.random.seed(seed)
    random.seed(seed)


set_seed()
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
for i in [theta for theta in [0, 90, 30]]:
    trans_lst.append(cv2.getRotationMatrix2D(center, i, scale))

    # for dir in ["train", "valid"]:
dataset = []
for path in os.listdir(DATA_DIR):
    path = os.path.join(DATA_DIR, path)
    with h5py.File(path, "r") as f:
        img = f["img"][:]
        label = f["label"][:]
        label_semaseg = np.zeros((label.shape[0], label.shape[1], 2))
        label_semaseg[:, :, 1] = label[:, :]
        label_semaseg[:, :, 0] = 1 - label[:, :]
        # plt.subplot(1, 2, 1)
        # plt.imshow(img)
        # plt.subplot(1, 2, 2)
        # plt.imshow(label)
        # plt.show()

    dataset.append((img, label_semaseg))
    # dataset.append((img, label))
    # plt.subplot(1, 2, 1)
    # plt.imshow(img)
    # plt.subplot(1, 2, 2)
    # plt.imshow(label)
    # plt.show()

random_idx = list(range(0, len(dataset) * 133 // 150))
random.shuffle(random_idx)
random_idx = random_idx + list(range(len(dataset) * 133 // 150, len(dataset)))
# print(random_idx)
# データをランダムに取得するためのインデックス
# random.shuffle(random_idx)
# データ取得。データ数が少ないため、auguentationを行う。回転、反転、明るさ調整を行い、学習データに追加。
for i, (img, label) in enumerate(tqdm(dataset)):
    if i < len(dataset) * 133 // 150:
        img_trans = img
        # img_trans = func.augment_brightness(img_trans)

        x_train.append(img_trans)
        y_train.append(cv2.resize(label, LABEL_SIZE))
        # print(label.shape, cv2.resize(label, LABEL_SIZE).shape)
        # img_trans = np.fliplr(img_trans)
        # img_trans = func.augment_brightness(img_trans)
        # x_train.append(img_trans)
        # y_train.append(cv2.resize(np.fliplr(label), LABEL_SIZE))

    else:
        x_valid.append(img)
        y_valid.append(cv2.resize(label, LABEL_SIZE))
# positive_count = 0
# for i, idx in enumerate(tqdm(random_idx)):
#     img, label = dataset[idx]
#     if i < len(random_idx) * 0.9:
#         # if np.sum(label) >= 6:
#         #     continue
#         # else:
#         #     continue
#         img_trans = img
#         img_trans = func.augment_brightness(img_trans)
#         x_train.append(img_trans)
#         y_train.append(cv2.resize(label, LABEL_SIZE))
#         img_trans = np.fliplr(img_trans)
#         img_trans = func.augment_brightness(img_trans)
#         x_train.append(img_trans)
#         y_train.append(cv2.resize(np.fliplr(label), LABEL_SIZE))

#     else:
#         x_valid.append(img)
#         y_valid.append(cv2.resize(label, LABEL_SIZE))
# break

# print(f"x_train: {len(x_train)}, x_test: {len(x_test)}, x_valid: {len(x_valid)}")

x_train = np.array(x_train) / 255
y_train = np.array(y_train)
x_test = np.array(x_test) / 255
y_test = np.array(y_test)
x_valid = np.array(x_valid) / 255
y_valid = np.array(y_valid)

# x_train = np.array(x_train)
# y_train = np.array(y_train)
# x_test = np.array(x_test)
# y_test = np.array(y_test)
# x_valid = np.array(x_valid)
# y_valid = np.array(y_valid)

# %%
"""
モデルの定義
"""

# mobilenet = Mobily

complessed_mobilenet = keras.models.load_model("model/trained_model.h5")
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
        BatchNormalization(),
        Conv2D(
            filters=32,
            kernel_size=1,
            strides=1,
            padding="same",
            activation="relu",
        ),
        BatchNormalization(),
        Conv2D(
            filters=2,
            kernel_size=1,
            strides=1,
            padding="same",
            activation="softmax",
            bias_initializer=tf.keras.initializers.Constant(value=0.0),
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
print(y_train.shape, y_valid.shape)
custom_model.compile(
    loss=loss.cross_loss,
    # loss=loss.DiceLoss,
    optimizer=Adam(learning_rate=0.001),
    metrics=[loss.IoU],
)
custom_model.fit(
    x_train,
    y_train,
    batch_size=32,
    epochs=200,
    validation_data=(x_valid, y_valid),
)


# %%

"""
テストデータでテスト
"""

test_dir = "test_result"
if os.path.exists(test_dir) == False:
    os.mkdir(test_dir)
else:
    import shutil

    shutil.rmtree(test_dir)
    os.mkdir(test_dir)
test_img_dir = "test"
for i, img in enumerate(tqdm(os.listdir(test_img_dir))):
    img = os.path.join(test_img_dir, img)
    img = cv2.imread(img)
    img = cv2.resize(img, INPUT_SIZE)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = np.array([img]) / 255
    pred = custom_model.predict(img)[0]
    # pred = np.argmax(pred, axis=2) #
    pred = pred[:, :, 1]
    # pred = np.array(pred * 255, dtype=np.uint8)
    # cv2.imwrite(os.path.join(test_dir, "result.png"), pred)
    plt.subplot(1, 2, 1)
    plt.imshow(img[0])
    plt.subplot(1, 2, 2)
    plt.imshow(pred, vmin=0, vmax=1)
    # plt.show()
    plt.savefig(os.path.join(test_dir, f"{i}.png"))
    plt.close()
    # break
# # %%
# """
# save Model
# """
# if os.path.exists(MODEL_DIR) == False:
#     os.mkdir(MODEL_DIR)

# custom_model.save(FULL_MODEL_PATH)
# conveter = tf.lite.TFLiteConverter.from_keras_model(custom_model)
# tflite_model = conveter.convert()
# float_model_size = len(tflite_model) / 1024 / 1024
# print(f"float model size: {float_model_size} MB")
# open(TFLITE_MODEL_PATH, "wb").write(tflite_model)


# import binascii


# def convert_to_c_array(bytes) -> str:
#     hexstr = binascii.hexlify(bytes).decode("UTF-8")
#     hexstr = hexstr.upper()
#     array = ["0x" + hexstr[i : i + 2] for i in range(0, len(hexstr), 2)]
#     array = [array[i : i + 10] for i in range(0, len(array), 10)]
#     return ",\n  ".join([", ".join(e) for e in array])


# tflite_binary = open(TFLITE_MODEL_PATH, "rb").read()
# ascii_bytes = convert_to_c_array(tflite_binary)
# header_file = (
#     "const unsigned char model_tflite[] = {\n  "
#     + ascii_bytes
#     + "\n};\nunsigned int model_tflite_len = "
#     + str(len(tflite_binary))
#     + ";"
# )
# # print(c_file)
# open(HEADER_MODEL_PATH, "w").write(header_file)
# open(SPRESENSE_HEADER_MODEL_PATH, "w").write(header_file)
# # %%
# print("--------start quantization--------")


# def representative_dataset_gen():
#     for i in range(len(x_valid)):
#         input_image = tf.cast(x_valid[i], tf.float32)
#         input_image = tf.reshape(
#             input_image, [1, INPUT_SIZE[0], INPUT_SIZE[1], INPUT_CHANNEL]
#         )
#         yield ([input_image])


# converter = tf.lite.TFLiteConverter.from_keras_model(custom_model)
# converter.optimizations = [tf.lite.Optimize.DEFAULT]
# converter.representative_dataset = representative_dataset_gen
# converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
# converter.inference_input_type = tf.int8
# converter.inference_output_type = tf.int8
# tflite_quant_model = converter.convert()

# tflite_quant_model_path = os.path.join(MODEL_DIR, "model_quant.tflite")
# with open(tflite_quant_model_path, "wb") as f:
#     f.write(tflite_quant_model)
# spresense_quant_model_path = os.path.join(MODEL_DIR, "spresense_model_quant.h")
# tflite_binary = open(tflite_quant_model_path, "rb").read()
# ascii_bytes = convert_to_c_array(tflite_binary)
# header_file = (
#     "const unsigned char model_tflite[] = {\n  "
#     + ascii_bytes
#     + "\n};\nunsigned int model_tflite_len = "
#     + str(len(tflite_binary))
#     + ";"
# )

# open(HEADER_QUANT_MODEL_PATH, "w").write(header_file)
# open(SPRESENSE_HEADER_QUANT_MODEL_PATH, "w").write(header_file)

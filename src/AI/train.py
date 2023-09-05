# %%

import tensorflow as tf
from keras.layers import (
    Dense,
    Input,
    GlobalAveragePooling2D,
    Dropout,
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
import tensorflow_model_optimization as tfmot
from keras import backend as K
from tqdm import tqdm
import os
import sys
import numpy as np
import h5py
import matplotlib.pyplot as plt
from module.const import *


# %%
# データセット
x_train = []
y_train = []
x_test = []
y_test = []
x_valid = []
y_valid = []

for dir in ["train", "test", "valid"]:
    dataset = []
    for i in tqdm(range(len(os.listdir(os.path.join(DATA_DIR, dir))))):
        with h5py.File(os.path.join(DATA_DIR, dir, str(i) + ".h5"), "r") as f:
            img = f["img"][:]
            label = f["label"][:]
        if np.all(label == 0):
            continue  # kuso detaset taisaku
        if dir == "train":
            x_train.append(img)
            y_train.append(label)
        elif dir == "test":
            x_test.append(img)
            y_test.append(label)
        elif dir == "valid":
            x_valid.append(img)
            y_valid.append(label)
print(f"x_train: {len(x_train)}, x_test: {len(x_test)}, x_valid: {len(x_valid)}")
x_train = np.array(x_train) / 127.5 - 1
y_train = np.array(y_train)
x_test = np.array(x_test) / 127.5 - 1
y_test = np.array(y_test)
x_valid = np.array(x_valid) / 127.5 - 1
y_valid = np.array(y_valid)

# %%
# モデルの定義
mobilenet = MobileNetV2(
    input_shape=(INPUT_SIZE[0], INPUT_SIZE[1], INPUT_CHANNEL),
    include_top=False,
    weights="imagenet",
)
mobilenet.summary()
complessed_mobilenet = Model(
    inputs=mobilenet.input, outputs=mobilenet.get_layer("block_6_expand_relu").output
)
for layer in complessed_mobilenet.layers:
    layer.trainable = False
custom_model = tf.keras.models.Sequential(
    [
        complessed_mobilenet,
        Conv2D(
            filters=52,
            kernel_size=1,
            strides=1,
            padding="same",
            activation="relu",
        ),
        # batchnorma
        tf.keras.layers.BatchNormalization(),
        Conv2D(
            filters=16,
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
        MaxPooling2D(pool_size=(2, 2)),  # max >> average
    ]
)
# combilned_output = Concatenate()([complessed_mobilenet.output, output_layers.output])
# 新しいモデルのサマリーを表示
# custom_model = Model(inputs=mobilenet.input, outputs=combilned_output)
custom_model.summary()
total_params = custom_model.count_params()
print("Total params: ", total_params)
print("Total RAM :", total_params * 4 / 1024 / 1024, "MB")  #


# %%
def IoU(targets, inputs, smooth=1e-6):
    batch = len(inputs)
    targets = tf.cast(targets, dtype=tf.float32)
    # inputs = K.softmax(inputs, axis=-1)
    inputs = tf.expand_dims(inputs, axis=-1)
    # inputs = MaxPooling2D(pool_size=(2, 2))(inputs)
    inputs = K.flatten(inputs)
    targets = K.flatten(targets)
    intersection = tf.reduce_sum(inputs * targets)
    iou = (intersection + smooth) / (
        K.sum(targets) + K.sum(inputs) - intersection + smooth
    )
    return iou


def weighted_focal_Loss(targets, inputs, beta=0.7, smooth=1e-6):
    # targets = targets.astye('float')
    # flatten label and prediction tensors
    # tf_show(inputs[0])
    batch = len(inputs)
    targets = tf.cast(targets, dtype=tf.float32)
    # inputs = K.softmax(inputs, axis=-1)
    inputs = tf.expand_dims(inputs, axis=-1)
    # inputs = MaxPooling2D(pool_size=(2, 2))(inputs)
    inputs = K.flatten(inputs)
    targets = K.flatten(targets)
    intersection = tf.reduce_sum(inputs * targets)
    precision = intersection / (K.sum(inputs) + smooth)
    recall = intersection / (K.sum(targets) + smooth)
    f = ((1 + beta**2) * precision * recall + smooth) / (
        beta**2 * precision + recall + smooth
    )
    return 1 - f


def DiceLoss(targets, inputs, smooth=1e-6):
    batch = len(inputs)
    targets = tf.cast(targets, dtype=tf.float32)
    # print(inputs.shape, targets.shape)
    inputs = tf.expand_dims(inputs, axis=-1)
    # inputs = MaxPooling2D(pool_size=(2, 2))(inputs)
    # inputs = K.softmax(inputs, axis=-1)
    inputs = K.flatten(inputs)
    targets = K.flatten(targets)
    intersection = tf.reduce_sum(
        inputs * targets
    )  # https://tensorflow.classcat.com/2018/09/07/tensorflow-tutorials-images-segmentation/
    # print(targets.shape, inputs.shape)
    dice = (2 * intersection + smooth) / (K.sum(targets) + K.sum(inputs) + smooth)
    return 1 - dice


# %%

custom_model.compile(
    loss=DiceLoss,
    optimizer=Adam(lr=0.010),
    metrics=[IoU],
)
custom_model.fit(
    x_train,
    y_train,
    batch_size=32,
    epochs=100,
    validation_data=(x_valid, y_valid),
)

# %%
# check model
for input, target in zip(x_test, y_test):
    input = np.expand_dims(input, axis=0)
    target = np.expand_dims(target, axis=0)
    pred = custom_model.predict(input)
    print(input.shape, target.shape, pred.shape)
    plt.subplot(1, 3, 1)
    plt.title("input")
    plt.imshow(input[0])
    plt.subplot(1, 3, 2)
    plt.imshow(target[0])
    plt.title("target")
    plt.subplot(1, 3, 3)
    plt.imshow(pred[0])
    plt.title("pred")
    plt.show()
# %%
# save model
conveter = tf.lite.TFLiteConverter.from_keras_model(custom_model)
tflite_model = conveter.convert()
float_model_size = len(tflite_model) / 1024 / 1024
print(f"float model size: {float_model_size} MB")
open("model.tflite", "wb").write(tflite_model)

# %%
import binascii


def convert_to_c_array(bytes) -> str:
    hexstr = binascii.hexlify(bytes).decode("UTF-8")
    hexstr = hexstr.upper()
    array = ["0x" + hexstr[i : i + 2] for i in range(0, len(hexstr), 2)]
    array = [array[i : i + 10] for i in range(0, len(array), 10)]
    return ",\n  ".join([", ".join(e) for e in array])


tflite_binary = open("model.tflite", "rb").read()
ascii_bytes = convert_to_c_array(tflite_binary)
header_file = (
    "const unsigned char model_tflite[] = {\n  "
    + ascii_bytes
    + "\n};\nunsigned int model_tflite_len = "
    + str(len(tflite_binary))
    + ";"
)
# print(c_file)
open("model_data.h", "w").write(header_file)

# %%

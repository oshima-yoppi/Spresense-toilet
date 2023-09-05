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
    Flatten,
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
        if dir == "train":
            x_train.append(img)
            y_train.append(label)
        elif dir == "test":
            x_test.append(img)
            y_test.append(label)
        elif dir == "valid":
            x_valid.append(img)
            y_valid.append(label)

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
complessed_mobilenet = Conv2D(
    filters=52,
    kernel_size=1,
    strides=1,
    padding="same",
    activation="relu",
)(complessed_mobilenet.output)
complessed_mobilenet = Conv2D(
    filters=16,
    kernel_size=1,
    strides=1,
    padding="same",
    activation="relu",
)(complessed_mobilenet)
complessed_mobilenet = Conv2D(
    filters=1, kernel_size=1, strides=1, padding="same", activation="sigmoid"
)(complessed_mobilenet)

# 新しいモデルのサマリーを表示
custom_model = Model(inputs=mobilenet.input, outputs=complessed_mobilenet)
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
    inputs = MaxPooling2D(pool_size=(2, 2))(inputs)
    inputs = K.flatten(inputs)
    targets = K.flatten(targets)
    intersection = tf.reduce_sum(inputs * targets)
    iou = (intersection + smooth) / (
        K.sum(targets) + K.sum(inputs) - intersection + smooth
    )
    return iou


def weighted_focal_Loss(targets, inputs, beta=0.5, smooth=1e-6):
    # targets = targets.astye('float')
    # flatten label and prediction tensors
    # tf_show(inputs[0])
    batch = len(inputs)
    targets = tf.cast(targets, dtype=tf.float32)
    # inputs = K.softmax(inputs, axis=-1)
    inputs = tf.expand_dims(inputs, axis=-1)
    inputs = MaxPooling2D(pool_size=(2, 2))(inputs)
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
    inputs = MaxPooling2D(pool_size=(2, 2))(inputs)
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
    loss=weighted_focal_Loss,
    optimizer=Adam(lr=0.01),
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
print(np.max(x_train[0]))

# %%

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
from module import func

# %%
# データセット
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

for dir in ["train", "valid"]:
    dataset = []
    for path in tqdm(os.listdir(os.path.join(DATA_DIR, dir))):
        path = os.path.join(DATA_DIR, dir, path)
        with h5py.File(path, "r") as f:
            img = f["img"][:]
            label = f["label"][:]
        # if np.all(label == 0):
        #     continue  # kuso detaset taisaku
        if dir == "train":
            for trans in trans_lst:
                img_trans = cv2.warpAffine(img, trans, INPUT_SIZE)
                label_trans = cv2.warpAffine(label, trans, INPUT_SIZE)
                x_train.append(img_trans)
                y_train.append(func.label_change(label_trans, ignore_haji=ignore))

                x_train.append(np.fliplr(img_trans))
                y_train.append(
                    func.label_change(np.fliplr(label_trans), ignore_haji=ignore)
                )

            # for k in range(4):
            #     img_rot = np.rot90(img, k=k)
            #     # print(img.shape, img_rot.shape)
            #     label_rot = np.rot90(label, k=k)
            #     x_train.append(img_rot)
            #     y_train.append(func.label_change(label_rot, ignore_haji=ignore))

            #     x_train.append(np.fliplr(img_rot))
            #     y_train.append(
            #         func.label_change(np.fliplr(label_rot), ignore_haji=ignore)
            #     )

            # print(label.shape, label_change(label).shape)
            # break

        elif dir == "test":
            x_test.append(img)
            # y_test.append(label)
            y_test.append(func.label_change(label, ignore_haji=ignore))
        elif dir == "valid":
            x_valid.append(img)
            # y_valid.append(label)
            y_valid.append(func.label_change(label, ignore_haji=ignore))
        # break
print(f"x_train: {len(x_train)}, x_test: {len(x_test)}, x_valid: {len(x_valid)}")
x_train = np.array(x_train) / 255
y_train = np.array(y_train)
x_test = np.array(x_test) / 255
y_test = np.array(y_test)
x_valid = np.array(x_valid) / 255
y_valid = np.array(y_valid)


def plot_augmentation_image(train_sample, params):
    # 同じ画像を16個複製する
    train_samples = np.repeat(
        train_sample.reshape((1, *train_sample.shape)), 16, axis=0
    )
    print(train_samples.shape)
    print(np.max(train_samples), np.min(train_samples))
    # 16個に対してparamsで与えられた変換を実施
    data_generator = keras.preprocessing.image.ImageDataGenerator(**params)
    generator = data_generator.flow(train_samples, batch_size=16)

    # 変換後のデータを取得
    batch_x = generator.next()

    # 変換後はfloat32となっているため、uint8に変換
    batch_x = batch_x.astype(np.uint8)

    # 描画処理
    plt.figure(figsize=(10, 10))
    for i in range(16):
        plt.subplot(4, 4, i + 1)
        plt.imshow(batch_x[i], vmin=0, vmax=1)
        plt.tick_params(labelbottom="off")
        plt.tick_params(labelleft="off")


# train_sample = x_train[0]
# plt.subplot(1, 2, 1)
# plt.imshow(train_sample)
# plt.subplot(1, 2, 2)
# plt.imshow(y_train[0])
# plt.show()
# print(train_sample.shape)
# params = {"rotation_range": 45}
# plot_augmentation_image(train_sample, params)

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

padding_h = 12 % LABEL_SIZE[0]
padding_w = 12 % LABEL_SIZE[1]
stride_h = (12 + padding_h * 2) // LABEL_SIZE[0]
stride_w = (12 + padding_w * 2) // LABEL_SIZE[1]
pool_h = (12 + padding_h * 2) // LABEL_SIZE[0]
pool_w = (12 + padding_w * 2) // LABEL_SIZE[1]

# poo_h, pool_w = 1, 1
custom_model = tf.keras.models.Sequential(
    [
        complessed_mobilenet,
        MaxPooling2D(
            pool_size=(pool_h, pool_w),
            strides=(stride_h, stride_w),
        ),  # max >> average 終盤に就けるより前の方がいい
        Conv2D(
            filters=128,
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
    # print(inputs.shape, targets.shape)
    # inputs = MaxPooling2D(pool_size=(2, 2))(inputs)
    # inputs = K.softmax(inputs, axis=-1)
    inputs = K.flatten(inputs)
    targets = K.flatten(targets)
    # print(inputs.shape, targets.shape)
    intersection = tf.reduce_sum(
        inputs * targets
    )  # https://tensorflow.classcat.com/2018/09/07/tensorflow-tutorials-images-segmentation/
    # print(targets.shape, inputs.shape)
    dice = (2 * intersection + smooth) / (K.sum(targets) + K.sum(inputs) + smooth)
    return 1 - dice


# %%

custom_model.compile(
    loss=DiceLoss,
    optimizer=Adam(learning_rate=0.001),
    metrics=[IoU],
)
custom_model.fit(
    x_train,
    y_train,
    batch_size=64,
    epochs=50,
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
    plt.imshow(input[0][..., ::-1])
    plt.subplot(1, 3, 2)
    plt.imshow(target[0])
    plt.title("target")
    plt.subplot(1, 3, 3)
    plt.imshow(pred[0])
    plt.title("pred")
    plt.show()
# %%
imgs = os.listdir("imgs")
# print(imgs)
# imgs.pop(0)
for img in imgs:
    img = cv2.imread(os.path.join("imgs", img))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (96, 96), interpolation=cv2.INTER_LINEAR)
    img = np.array([img]) / 255
    print(img.shape)
    pred = custom_model.predict(img)
    img = func.draw_line(img[0])
    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.subplot(1, 2, 2)
    plt.imshow(pred[0])
    plt.show()
# %%
# imgs = os.listdir("imgs")
# for img in imgs:
#     img = cv2.imread(os.path.join("imgs", img))
#     plt.subplot(1, 2, 1)
#     plt.imshow(img[..., ::-1])
#     img = cv2.resize(img, (96, 96), interpolation=cv2.INTER_LINEAR)
#     img = np.array([img])
#     # img = np.array(img)
#     print(img.shape)
#     plt.subplot(1, 2, 2)
#     plt.imshow(img[0][..., ::-1])
#     plt.show()
# %%
# save model
custom_model.save("full_model.h5")
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

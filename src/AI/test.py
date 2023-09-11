import tensorflow as tf
import os
import h5py
import numpy as np
from matplotlib import pyplot as plt
import cv2


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


model = tf.lite.Interpreter(model_path="model.tflite")
# model = tf.keras.models.load_model(
#     "full_model.h5",
# )
# model.summary()
imgs = os.listdir("imgs")
for img in imgs:
    img = cv2.imread(os.path.join("imgs", img))
    img = cv2.resize(img, (96, 96))
    img = np.array([img]) / 127.5 - 1
    pred = model.predict(img)
    plt.subplot(1, 2, 1)
    plt.imshow(img[0])
    plt.subplot(1, 2, 2)
    plt.imshow(pred[0])
    plt.show()

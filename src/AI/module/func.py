from module.const import *
import numpy as np
import cv2
import tensorflow as tf
import tensorflow.keras.backend as K
from tensorflow.keras.layers import Layer


def label_change(label, ignore_haji=False):
    label_output = np.zeros(LABEL_SIZE)
    for i in range(label.shape[0]):
        for j in range(label.shape[1]):
            if label[i, j] == 1:
                # print(2222222222)
                label_output[
                    int(i / label.shape[0] * LABEL_SIZE[0]),
                    int(j / label.shape[1] * LABEL_SIZE[1]),
                ] = 1.0

    if ignore_haji:
        for i in [0, LABEL_SIZE[0] - 1]:
            for j in range(LABEL_SIZE[1]):
                label_output[i, j] = 0.0
        for j in [0, LABEL_SIZE[1] - 1]:
            for i in range(LABEL_SIZE[0]):
                label_output[i, j] = 0.0
    return label_output


def augment_brightness(image, brightness_range=(0.5, 2.0)):
    # 明るさをランダムに調整
    brightness_factor = np.random.uniform(brightness_range[0], brightness_range[1])
    augmented_image = cv2.convertScaleAbs(image, alpha=brightness_factor, beta=0)

    return augmented_image


def draw_line(img):
    height, width, _ = img.shape

    cell_width = width // LABEL_SIZE[1]
    cell_height = height // LABEL_SIZE[0]
    for x in range(1, LABEL_SIZE[1]):
        cv2.line(img, (x * cell_width, 0), (x * cell_width, height), (0, 255, 255))
    for y in range(1, LABEL_SIZE[0]):
        cv2.line(img, (0, y * cell_height), (width, y * cell_height), (0, 255, 255))
    return img

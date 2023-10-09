from module.const import *
import numpy as np
import cv2
import tensorflow as tf
import tensorflow.keras.backend as K
from tensorflow.keras.layers import Layer


# def label_change(label, ignore_haji=False):
#     label_output = cv2.resize(label, LABEL_SIZE)
#     return label_output


def convert_label(label, output_size):
    # labelをoutput_sizeに変換する
    output_label = np.zeros(output_size)
    height, width = label.shape
    cell_width = width // output_size[1]
    cell_height = height // output_size[0]
    for i in range(output_size[0]):
        for j in range(output_size[1]):
            if np.any(
                label[
                    i * cell_height : (i + 1) * cell_height,
                    j * cell_width : (j + 1) * cell_width,
                ]
                == 1
            ):
                output_label[i, j] = 1
    return output_label


def split_img(img, split_num=SPLIT_NUM):
    # 画像を分割する
    if len(img.shape) == 2:
        height, width = img.shape
    else:
        height, width, _ = img.shape
    cell_width = width // split_num
    cell_height = height // split_num
    splited_img_lst = []
    for i in range(split_num):
        for j in range(split_num):
            splited_img_lst.append(
                img[
                    cell_height * i : cell_height * (i + 1),
                    cell_width * j : cell_width * (j + 1),
                ]
            )
    return splited_img_lst


def augment_brightness(image, brightness_range=(0.5, 2.0)):
    # 明るさをランダムに調整
    brightness_factor = np.random.uniform(brightness_range[0], brightness_range[1])
    augmented_image = cv2.convertScaleAbs(image, alpha=brightness_factor, beta=0)

    return augmented_image


def draw_line(img):
    height, width = img.shape[:2]

    cell_width = width // LABEL_SIZE[1]
    cell_height = height // LABEL_SIZE[0]
    if img.max() <= 1:
        for x in range(1, LABEL_SIZE[1]):
            cv2.line(img, (x * cell_width, 0), (x * cell_width, height), (0, 1, 1))
        for y in range(1, LABEL_SIZE[0]):
            cv2.line(img, (0, y * cell_height), (width, y * cell_height), (0, 1, 1))
    else:
        for x in range(1, LABEL_SIZE[1]):
            cv2.line(img, (x * cell_width, 0), (x * cell_width, height), (0, 255, 255))
        for y in range(1, LABEL_SIZE[0]):
            cv2.line(img, (0, y * cell_height), (width, y * cell_height), (0, 255, 255))
    return img

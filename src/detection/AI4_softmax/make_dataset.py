import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pathlib
import cv2
import shutil
import h5py
from tqdm import tqdm
from module.const import *
import re
from module import func


def write_label(label_path, output_size):
    label = np.zeros(output_size)
    with open(label_path, "r") as f:
        for line in f:
            line = line.split(" ")
            line = [float(x) for x in line]
            x, y, w, h = line[1:]
            x = int(x * output_size[1])
            y = int(y * output_size[0])
            label[y, x] = 1
    return label


def crop_center(img, width, height):
    # 画像のサイズを取得
    img_height, img_width = img.shape[:2]

    # 切り取りの開始座標を計算
    left = (img_width - width) // 2
    top = (img_height - height) // 2

    # 切り取り範囲を指定
    right = left + width
    bottom = top + height

    # 画像を切り取る
    cropped_img = img[top:bottom, left:right]
    return cropped_img


def crop_img(img, crop_size):
    img_height, img_width = img.shape[:2]
    output_height, output_width = crop_size
    x_crop_num = img_width // output_width
    y_crop_num = img_height // output_height
    for i in range(x_crop_num):
        for j in range(y_crop_num):
            x_start = i * output_width
            x_end = (i + 1) * output_width
            y_start = j * output_height
            y_end = (j + 1) * output_height
            yield img[y_start:y_end, x_start:x_end]


if __name__ == "__main__":
    if os.path.exists(DATA_DIR):
        shutil.rmtree(DATA_DIR)
    os.makedirs(DATA_DIR)

    train_dir = "rawdata/train"
    img_train_pathes = os.listdir(os.path.join(train_dir, "images"))
    label_train_pathes = os.listdir(os.path.join(train_dir, "labels"))

    count = 0
    kind = set()
    for img_path, label_path in zip(tqdm(img_train_pathes), label_train_pathes):
        img_path = os.path.join(train_dir, "images", img_path)
        label_path = os.path.join(train_dir, "labels", label_path)

        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        small_rate = 0.25
        small_height = int(img.shape[0] * small_rate)
        small_width = int(img.shape[1] * small_rate)
        small_img = cv2.resize(img, (small_width, small_height))
        small_label = write_label(label_path, (small_height, small_width))

        # plt.subplot(1, 2, 1)
        # plt.imshow(small_img)
        # plt.subplot(1, 2, 2)
        # plt.imshow(small_label)
        # plt.show()
        center_crop_img = crop_center(small_img, INPUT_SIZE[0], INPUT_SIZE[1])
        center_crop_label = crop_center(small_label, INPUT_SIZE[0], INPUT_SIZE[1])
        center_crop_label = func.convert_label(center_crop_label, LABEL_SIZE)
        # print(center_crop_img.shape)
        if center_crop_img.shape[:2] != INPUT_SIZE:
            continue
        save_path = os.path.join(DATA_DIR, str(count) + ".h5")
        # plt.subplot(1, 2, 1)
        # plt.imshow(center_crop_img)
        # plt.subplot(1, 2, 2)
        # plt.imshow(center_crop_label)
        # plt.show()

        gray = cv2.cvtColor(center_crop_img, cv2.COLOR_RGB2GRAY)
        center_crop_img = np.stack([gray, gray, gray], axis=-1)

        with h5py.File(save_path, "w") as f:
            f.create_dataset("img", data=center_crop_img)
            f.create_dataset("label", data=center_crop_label)
            # print(f"save: {save_path}")
        count += 1

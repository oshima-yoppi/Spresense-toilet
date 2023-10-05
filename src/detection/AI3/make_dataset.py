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


def read_label(label_path, output_size):
    label = np.zeros(output_size)
    with open(label_path, "r") as f:
        for line in f:
            line = line.split(" ")
            line = [float(x) for x in line]
            x, y, w, h = line[1:]
            x_start = int((x - w / 2) * output_size[1])
            x_end = int((x + w / 2) * output_size[1])
            y_start = int((y - h / 2) * output_size[0])
            y_end = int((y + h / 2) * output_size[0])
            label[y_start:y_end, x_start:x_end] = 1

    return label


def write_label_circle(label_path, output_size):
    label = np.zeros(output_size)
    with open(label_path, "r") as f:
        for line in f:
            line = line.split(" ")
            line = [float(x) for x in line]
            x, y, w, h = line[1:]
            x = int(x * output_size[1])
            y = int(y * output_size[0])
            x_axis = int(w * output_size[1] // 2)
            y_axis = int(h * output_size[0] // 2)
            cv2.ellipse(label, (x, y), (x_axis, y_axis), 0, 0, 360, 1, -1)
    return label


def crop_center(img, rate=0.05):
    # 画像のサイズを取得
    img_height, img_width = img.shape[:2]
    start_x = int(img_width * rate)
    start_y = int(img_height * rate)
    end_x = int(img_width * (1 - rate))
    end_y = int(img_height * (1 - rate))
    # 画像を切り取る
    cropped_img = img[start_y:end_y, start_x:end_x]
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
        small_label = write_label_circle(label_path, (small_height, small_width))
        small_img = crop_center(small_img)
        small_label = crop_center(small_label)

        # print(small_img.shape, small_label.shape)
        for cropped_img, cropped_label in zip(
            crop_img(small_img, INPUT_SIZE), crop_img(small_label, INPUT_SIZE)
        ):
            if cropped_img.shape[:2] != INPUT_SIZE:
                continue

            save_path = os.path.join(DATA_DIR, str(count) + ".h5")
            with h5py.File(save_path, "w") as f:
                f.create_dataset("img", data=cropped_img)
                f.create_dataset("label", data=cropped_label)
            count += 1

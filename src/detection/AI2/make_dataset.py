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

        with h5py.File(save_path, "w") as f:
            f.create_dataset("img", data=center_crop_img)
            f.create_dataset("label", data=center_crop_label)
            # print(f"save: {save_path}")
        count += 1
        # plt.subplot(1, 2, 1)
        # plt.imshow(img)
        # plt.subplot(1, 2, 2)
        # plt.imshow(center_crop_label)
        # plt.show()

        # break
    # print(kind)

    # count = 0
    # IMAGE_DIR = os.path.join(RAW_DATA_DIR, "images")
    # MASK_DIR = os.path.join(RAW_DATA_DIR, "masks")
    # image_filepaths = os.listdir(IMAGE_DIR)
    # mask_filepaths = os.listdir(MASK_DIR)

    # for _, img_path in enumerate(tqdm(image_filepaths)):
    #     # if i % 10 == 0:
    #     #     pass
    #     # else:
    #     #     continue
    #     number = re.findall(r"\d+", img_path)[0]
    #     mask_path = "IMG_" + number + ".png"
    #     mask_path = os.path.join(MASK_DIR, mask_path)
    #     img_path = os.path.join(IMAGE_DIR, img_path)

    #     img = cv2.imread(img_path)
    #     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #     mask = cv2.imread(mask_path)
    #     label = np.zeros((mask.shape[0], mask.shape[1]))
    #     for i in range(mask.shape[0]):
    #         for j in range(mask.shape[1]):
    #             if mask[i][j][0] == 255:
    #                 label[i][j] = 1

    #     splited_img_lst = func.split_img(img)
    #     splited_label_lst = func.split_img(label)
    #     for splited_img, splited_label in zip(splited_img_lst, splited_label_lst):
    #         splited_img = cv2.resize(splited_img, INPUT_SIZE)
    #         splited_label = cv2.resize(splited_label, INPUT_SIZE)
    #         save_path = os.path.join(DATA_DIR, str(count) + ".h5")
    #         with h5py.File(save_path, "w") as f:
    #             f.create_dataset("img", data=splited_img)
    #             f.create_dataset("label", data=splited_label)
    #             # print(f"save: {save_path}")
    #         count += 1

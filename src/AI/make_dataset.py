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


if os.path.exists(DATA_DIR):
    shutil.rmtree(DATA_DIR)
os.makedirs(DATA_DIR)

count = 0
IMAGE_DIR = os.path.join(RAW_DATA_DIR, "images")
ANNOTATION_DIR = os.path.join(RAW_DATA_DIR, "annotations")
image_filepaths = os.listdir(IMAGE_DIR)
annotation_filepaths = os.listdir(ANNOTATION_DIR)
for i, (image_filepath, annotation_filepath) in enumerate(
    zip(tqdm(image_filepaths), annotation_filepaths)
):
    image_filepath = os.path.join(IMAGE_DIR, image_filepath)
    annotation_filepath = os.path.join(ANNOTATION_DIR, annotation_filepath)
    image = cv2.imread(image_filepath)

    with open(annotation_filepath, "r") as f:
        sentenses = f.readlines()
    boxes = []
    centroids = []

    height, width, _ = image.shape
    # print(height, width)
    for sentense in sentenses:
        _, x, y, w, h = map(float, sentense.split())
        # print(x, y, w, h)
        x1 = int(x * width - w * width / 2)
        y1 = int(y * height - h * height / 2)
        x2 = int(x * width + w * width / 2)
        y2 = int(y * height + h * height / 2)
        boxes.append([x1, y1, x2, y2])
        centroids.append((int(x * width), int(y * height)))

    image = cv2.resize(image, INPUT_SIZE)
    label = np.zeros(INPUT_SIZE)

    for x, y in centroids:
        # ここでのx, yは画像の座標.ｘは横方向、ｙは縦方向
        x_resized = int(x / width * INPUT_SIZE[0])
        y_resized = int(y / height * INPUT_SIZE[1])
        label[y_resized, x_resized] = 1

    save_data_path = os.path.join(DATA_DIR, str(i) + ".h5")
    with h5py.File(save_data_path, "w") as f:
        f.create_dataset("img", data=image)
        f.create_dataset("label", data=label)


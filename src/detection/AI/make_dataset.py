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

if os.path.exists(DATA_DIR):
    shutil.rmtree(DATA_DIR)
os.makedirs(DATA_DIR)

count = 0
IMAGE_DIR = os.path.join(RAW_DATA_DIR, "images")
MASK_DIR = os.path.join(RAW_DATA_DIR, "masks")
image_filepaths = os.listdir(IMAGE_DIR)
mask_filepaths = os.listdir(MASK_DIR)

for _, img_path in enumerate(tqdm(image_filepaths)):
    # if i % 10 == 0:
    #     pass
    # else:
    #     continue
    number = re.findall(r"\d+", img_path)[0]
    mask_path = "IMG_" + number + ".png"
    mask_path = os.path.join(MASK_DIR, mask_path)
    img_path = os.path.join(IMAGE_DIR, img_path)

    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mask = cv2.imread(mask_path)
    label = np.zeros((mask.shape[0], mask.shape[1]))
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            if mask[i][j][0] == 255:
                label[i][j] = 1

    splited_img_lst = func.split_img(img)
    splited_label_lst = func.split_img(label)
    for splited_img, splited_label in zip(splited_img_lst, splited_label_lst):
        splited_img = cv2.resize(splited_img, INPUT_SIZE)
        splited_label = cv2.resize(splited_label, INPUT_SIZE)
        save_path = os.path.join(DATA_DIR, str(count) + ".h5")
        with h5py.File(save_path, "w") as f:
            f.create_dataset("img", data=splited_img)
            f.create_dataset("label", data=splited_label)
            # print(f"save: {save_path}")
        count += 1

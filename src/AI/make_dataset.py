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


RAW_DATA_DIR = "rawdata"
NEW_DATA_DIR = "data"
NEW_TRAIN_DIR = os.path.join(NEW_DATA_DIR, "train")
NEW_TEST_DIR = os.path.join(NEW_DATA_DIR, "test")
NEW_VALID_DIR = os.path.join(NEW_DATA_DIR, "valid")
if os.path.exists(NEW_DATA_DIR):
    shutil.rmtree(NEW_DATA_DIR)
os.mkdir(NEW_DATA_DIR)

for dir in ["train", "test", "valid"]:
    os.mkdir(os.path.join(NEW_DATA_DIR, dir))
    img_dir = os.path.join(RAW_DATA_DIR, dir, "images")
    label_dir = os.path.join(RAW_DATA_DIR, dir, "labels")

    img_filenames = os.listdir(img_dir)
    label_filenames = os.listdir(label_dir)
    for i, (img_filename, label_filename) in enumerate(
        zip(tqdm(img_filenames), label_filenames)
    ):
        img_path = os.path.join(img_dir, img_filename)
        label_path = os.path.join(label_dir, label_filename)
        img = cv2.imread(img_path)
        label = np.zeros(LABEL_SIZE)
        with open(label_path, "r") as f:
            sentenses = f.readlines()
        for sentense in sentenses:
            _, y, x, w, h = map(float, sentense.split())
            label[int(x * LABEL_SIZE[0]), int(y * LABEL_SIZE[1])] = 1
        img = cv2.resize(img, INPUT_SIZE)
        # label = cv2.resize(label, LABEL_SIZE)

        save_filename = str(i) + ".h5"
        save_path = os.path.join(NEW_DATA_DIR, dir, save_filename)
        with h5py.File(save_path, "w") as f:
            f.create_dataset("img", data=img)
            f.create_dataset("label", data=label)

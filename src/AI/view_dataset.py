import h5py
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from tqdm import tqdm
from module.const import *
from module import func
import shutil


save_dir = "check_data"
if os.path.exists(save_dir):
    shutil.rmtree(save_dir)
os.makedirs(save_dir)
for i, path in enumerate(tqdm(os.listdir(DATA_DIR))):
    path = os.path.join(DATA_DIR,  path)
    #     continue
    with h5py.File(path, "r") as f:
        img = f["img"][:]
        label = f["label"][:]

    label = func.label_change(label, False)
    plt.subplot(1, 2, 1)
    plt.imshow(img[..., ::-1])
    plt.subplot(1, 2, 2)
    plt.imshow(label)
    save_path = os.path.join(save_dir, str(i) + ".png")
    plt.savefig(save_path)
    plt.close()

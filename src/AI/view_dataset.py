import h5py
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from tqdm import tqdm
from module.const import *
from module import func

for i, path in enumerate(os.listdir(os.path.join(DATA_DIR, "train"))):
    path = os.path.join(DATA_DIR, "train", path)
    #     continue
    with h5py.File(path, "r") as f:
        img = f["img"][:]
        label = f["label"][:]

    label = func.label_change(label)
    plt.subplot(1, 2, 1)
    plt.imshow(img[..., ::-1])
    plt.subplot(1, 2, 2)
    plt.imshow(label)
    plt.savefig(f"gomi/{i}.png")

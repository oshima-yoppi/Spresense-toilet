import h5py
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from tqdm import tqdm
from module.const import *

for i in range(len(os.listdir(os.path.join(DATA_DIR, "train")))):
    # if i < 100:
    #     continue
    with h5py.File(os.path.join(DATA_DIR, "train", f"{i}.h5"), "r") as f:
        img = f["img"][:]
        label = f["label"][:]
    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.subplot(1, 2, 2)
    plt.imshow(label)
    plt.savefig(f"gomi/{i}.png")

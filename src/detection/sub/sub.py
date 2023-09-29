import cv2
import os
from matplotlib import pyplot as plt
import numpy as np
from module import func
from module.const import *

basepath = "base.jpg"
imgpath1 = os.path.join("1.jpg")
imgpath2 = os.path.join("2.jpg")


base = cv2.imread(basepath)
base = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY)
img1 = cv2.imread(imgpath1)
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2 = cv2.imread(imgpath2)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

base = cv2.resize(base, IMG_SIZE)
img1 = cv2.resize(img1, IMG_SIZE)
img2 = cv2.resize(img2, IMG_SIZE)


dif1 = func.get_diff(base, img1)
dif2 = func.get_diff(base, img2)

th = 60
dif1_mask = func.get_diff_mask(dif1, th)
dif2_mask = func.get_diff_mask(dif2, th)

plt.subplot(1, 4, 1)
plt.imshow(base)
plt.subplot(1, 4, 2)
plt.imshow(img2)
plt.subplot(1, 4, 3)
plt.imshow(dif2)
plt.subplot(1, 4, 4)
plt.imshow(dif2_mask)
plt.show()


matchinger = func.CircleMaching(radius=6)
res1 = matchinger.get_maching(dif1_mask)
res2 = matchinger.get_maching(dif2_mask)

mask1 = matchinger.get_mask(res1, th=0.5)
mask2 = matchinger.get_mask(res2, th=0.5)

plt.subplot(2, 4, 1)
plt.imshow(img1)
plt.subplot(2, 4, 2)
plt.imshow(dif1)
plt.subplot(2, 4, 3)
plt.imshow(res1)
plt.subplot(2, 4, 4)
plt.imshow(mask1)
plt.subplot(2, 4, 5)
plt.imshow(img2)
plt.subplot(2, 4, 6)
plt.imshow(dif2)
plt.subplot(2, 4, 7)
plt.imshow(res2)
plt.subplot(2, 4, 8)
plt.imshow(mask2)
plt.show()

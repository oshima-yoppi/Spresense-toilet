import cv2
import os
from matplotlib import pyplot as plt

imgpath1 = os.path.join("rawdata/images", "IMG_5451.jpeg")
imgpath2 = os.path.join("rawdata/images", "IMG_5457.jpeg")


img1 = cv2.imread(imgpath1)
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

img2 = cv2.imread(imgpath2)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

sabun = img1.astype(int) - img2.astype(int)

plt.subplot(1, 3, 1)
plt.imshow(img1)
plt.subplot(1, 3, 2)
plt.imshow(img2)
plt.subplot(1, 3, 3)
plt.imshow(sabun)
plt.show()

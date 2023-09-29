import cv2
import os
from matplotlib import pyplot as plt
import numpy as np

IMG_SIZE = (96, 96)

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


sabun1 = base.astype(int) - img1.astype(int)
sabun2 = base.astype(int) - img2.astype(int)
sabun1 = np.abs(sabun1)
sabun2 = np.abs(sabun2)

th = 60
sabun1 = np.where(sabun1 > th, 1, 0)
sabun2 = np.where(sabun2 > th, 1, 0)

# plt.subplot(1, 5, 1)
# plt.imshow(base)
# plt.subplot(1, 5, 2)
# plt.imshow(img1)
# plt.subplot(1, 5, 3)
# plt.imshow(sabun1)
# plt.subplot(1, 5, 4)
# plt.imshow(img2)
# plt.subplot(1, 5, 5)
# plt.imshow(sabun2)
# plt.show()

sabun1 = sabun1.astype(np.uint8)
radius = 6  # 半円の半径を設定
filter_size = (2 * radius, 2 * radius)  # フィルタのサイズを計算
half_circle_filter = np.zeros(filter_size, dtype=np.uint8)
# half_circle_filter = np.full(filter_size, 1, dtype=np.uint8)
cv2.ellipse(
    half_circle_filter, (radius, radius), (radius, radius), 0, 180, 360, 255, -1
)

# plt.imshow(half_circle_filter)
# plt.show()
res = cv2.matchTemplate(sabun1, half_circle_filter, cv2.TM_CCOEFF_NORMED)

plt.subplot(1, 4, 1)
plt.imshow(sabun1)
plt.subplot(1, 4, 2)
plt.imshow(half_circle_filter)
plt.subplot(1, 4, 3)
plt.imshow(res)
plt.subplot(1, 4, 4)
plt.imshow(np.where(res > 0.5, 1, 0))
plt.show()

# # 半円を描画する
# cv2.ellipse(
#     half_circle_filter, (radius, radius), (radius, radius), 0, 180, 360, 255, -1
# )

# # フィルタを正規化する
# half_circle_filter = half_circle_filter / 255.0


# # 画像とフィルタを畳み込む
# filtered_image = cv2.filter2D(sabun1, -1, half_circle_filter)

# # 結果を表示する
# plt.subplot(1, 2, 1)
# plt.imshow(sabun1)
# plt.subplot(1, 2, 2)
# plt.imshow(filtered_image)
# plt.show()

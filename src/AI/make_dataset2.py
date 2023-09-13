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

# from pycocotools.coco import COCO

RAW_DATA_DIR = "rawdata5"  # 4 coco, 5 video
NEW_DATA_DIR = "data5"
if os.path.exists(NEW_DATA_DIR):
    shutil.rmtree(NEW_DATA_DIR)
os.makedirs(NEW_DATA_DIR)

count = 0
IMAGE_DIR = os.path.join(RAW_DATA_DIR, "images")
ANNOTATION_DIR = os.path.join(RAW_DATA_DIR, "annotations")
image_filepaths = os.listdir(IMAGE_DIR)
annotation_filepaths = os.listdir(ANNOTATION_DIR)
for i, (image_filepath, annotation_filepath) in enumerate(
    zip(tqdm(image_filepaths), annotation_filepaths)
):
    # if i % 10 != 0:
    #     continue
    # print(image_filepath, annotation_filepath)
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
    # labeled_image = image.copy()
    # print(boxes)
    # for box, centroid in zip(boxes, centroids):
    #     x1, y1, x2, y2 = map(int, box)
    #     c1, c2 = centroid
    #     print(x1, y1, x2, y2)
    #     # cv2.rectangle(labeled_image, (y1, x1), (y2, x2), (0, 255, 0), 2)
    #     cv2.rectangle(labeled_image, (x1, y1), (x2, y2), (0, 255, 0), 20)
    #     cv2.circle(labeled_image, (c1, c2), 10, (0, 0, 255), -1)
    # if len(boxes) == 0:
    #     continue

    # plt.subplot(1, 2, 1)
    # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # plt.subplot(1, 2, 2)
    # plt.imshow(cv2.cvtColor(labeled_image, cv2.COLOR_BGR2RGB))
    # plt.show()
    image = cv2.resize(image, INPUT_SIZE)
    label = np.zeros(INPUT_SIZE)

    for x, y in centroids:
        # ここでのx, yは画像の座標.ｘは横方向、ｙは縦方向
        x_resized = int(x / width * INPUT_SIZE[0])
        y_resized = int(y / height * INPUT_SIZE[1])
        label[y_resized, x_resized] = 1
    # plt.subplot(1, 2, 1)
    # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # plt.subplot(1, 2, 2)
    # plt.imshow(label)
    # plt.show()
    save_data_path = os.path.join(NEW_DATA_DIR, str(i) + ".h5")
    with h5py.File(save_data_path, "w") as f:
        f.create_dataset("img", data=image)
        f.create_dataset("label", data=label)

    # exit()
# annotation_path = os.path.join(RAW_DATA_DIR + "/_annotations.json")
# coco = COCO(annotation_path)
# categorise = coco.loadCats(coco.getCatIds())
# category_names = [c["name"] for c in categorise]
# print(f"category_names: {category_names}")
# image_ids = coco.getImgIds()
# print(f"image_ids: {image_ids}")
# for image_id in tqdm(image_ids):
#     # image_id = image_ids[0]
#     image = coco.loadImgs(image_id)[0]
#     image_info = coco.loadImgs(image_id)[0]
#     annotations = coco.loadAnns(coco.getAnnIds(imgIds=image_id))
#     # print(f"画像情報: {image_info}")
#     # print(f"アノテーション情報: {annotations}")
#     boxes = []
#     for annotation in annotations:
#         x, y, w, h = annotation["bbox"]
#         boxes.append([x, y, x + w, y + h])
#     boxes = np.array(boxes)
#     # print(f"boxes: {boxes}")
#     image_annnotate = cv2.imread(
#         os.path.join(RAW_DATA_DIR, witch, image_info["file_name"])
#     )

#     image = cv2.imread(os.path.join(RAW_DATA_DIR, witch, image_info["file_name"]))
#     if image is None:
#         continue
#     image = cv2.resize(image, INPUT_SIZE)
#     label = np.zeros(INPUT_SIZE)
#     centroids = []
#     image_width = image_info["width"]
#     image_height = image_info["height"]
#     for box in boxes:
#         x1, y1, x2, y2 = map(int, box)
#         centroids.append([(x1 + x2) / 2, (y1 + y2) / 2])
#     for centroid in centroids:
#         x, y = centroid
#         x = int(x / image_width * INPUT_SIZE[0])
#         y = int(y / image_height * INPUT_SIZE[1])
#         label[y, x] = 1
#     save_data_path = os.path.join(NEW_DATA_DIR, witch, str(image_id) + ".h5")
#     with h5py.File(save_data_path, "w") as f:
#         f.create_dataset("img", data=image)
#         f.create_dataset("label", data=label)
# # 出力確認用
# for box in boxes:
#     x1, y1, x2, y2 = map(int, box)
#     cv2.rectangle(image_annnotate, (x1, y1), (x2, y2), (0, 0, 255), 2)

# plt.subplot(1, 2, 1)
# plt.imshow(cv2.cvtColor(image_annnotate, cv2.COLOR_BGR2RGB))
# plt.subplot(1, 2, 2)
# plt.imshow(label)
# plt.show()
# exit()


# for dir in ["train", "test", "valid"]:
#     os.mkdir(os.path.join(NEW_DATA_DIR, dir))
#     img_dir = os.path.join(RAW_DATA_DIR, dir, "images")
#     label_dir = os.path.join(RAW_DATA_DIR, dir, "labels")

#     img_filenames = os.listdir(img_dir)
#     label_filenames = os.listdir(label_dir)
#     for i, (img_filename, label_filename) in enumerate(
#         zip(tqdm(img_filenames), label_filenames)
#     ):
#         img_path = os.path.join(img_dir, img_filename)
#         label_path = os.path.join(label_dir, label_filename)
#         img = cv2.imread(img_path)
#         label = np.zeros(LABEL_SIZE)
#         with open(label_path, "r") as f:
#             sentenses = f.readlines()
#         for sentense in sentenses:
#             _, y, x, w, h = map(float, sentense.split())
#             label[int(x * LABEL_SIZE[0]), int(y * LABEL_SIZE[1])] = 1
#         img = cv2.resize(img, INPUT_SIZE)
#         # label = cv2.resize(label, LABEL_SIZE)

#         save_filename = str(i) + ".h5"
#         save_path = os.path.join(NEW_DATA_DIR, dir, save_filename)
#         with h5py.File(save_path, "w") as f:
#             f.create_dataset("img", data=img)
#             f.create_dataset("label", data=label)

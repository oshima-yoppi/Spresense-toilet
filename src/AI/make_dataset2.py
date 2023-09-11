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
from pycocotools.coco import COCO

RAW_DATA_DIR = "rawdata4_"  # 4 coco
NEW_DATA_DIR = "data4"
new_dirs = [os.path.join(NEW_DATA_DIR, dir) for dir in ["train", "valid"]]
for new_dir in new_dirs:
    if os.path.exists(new_dir):
        shutil.rmtree(new_dir)
    os.makedirs(new_dir)

count = 0
for witch in ["train", "valid"]:
    annotation_path = os.path.join(RAW_DATA_DIR, witch + "/_annotations.coco.json")
    coco = COCO(annotation_path)
    categorise = coco.loadCats(coco.getCatIds())
    category_names = [c["name"] for c in categorise]
    print(f"category_names: {category_names}")
    image_ids = coco.getImgIds()
    print(f"image_ids: {image_ids}")
    for image_id in tqdm(image_ids):
        # image_id = image_ids[0]
        image = coco.loadImgs(image_id)[0]
        image_info = coco.loadImgs(image_id)[0]
        annotations = coco.loadAnns(coco.getAnnIds(imgIds=image_id))
        # print(f"画像情報: {image_info}")
        # print(f"アノテーション情報: {annotations}")
        boxes = []
        for annotation in annotations:
            x, y, w, h = annotation["bbox"]
            boxes.append([x, y, x + w, y + h])
        boxes = np.array(boxes)
        # print(f"boxes: {boxes}")
        image_annnotate = cv2.imread(
            os.path.join(RAW_DATA_DIR, witch, image_info["file_name"])
        )

        image = cv2.imread(os.path.join(RAW_DATA_DIR, witch, image_info["file_name"]))
        if image is None:
            continue
        image = cv2.resize(image, INPUT_SIZE)
        label = np.zeros(INPUT_SIZE)
        centroids = []
        image_width = image_info["width"]
        image_height = image_info["height"]
        for box in boxes:
            x1, y1, x2, y2 = map(int, box)
            centroids.append([(x1 + x2) / 2, (y1 + y2) / 2])
        for centroid in centroids:
            x, y = centroid
            x = int(x / image_width * INPUT_SIZE[0])
            y = int(y / image_height * INPUT_SIZE[1])
            label[y, x] = 1
        save_data_path = os.path.join(NEW_DATA_DIR, witch, str(image_id) + ".h5")
        with h5py.File(save_data_path, "w") as f:
            f.create_dataset("img", data=image)
            f.create_dataset("label", data=label)
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

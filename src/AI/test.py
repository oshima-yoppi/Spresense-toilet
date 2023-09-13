import tensorflow as tf
import os
import h5py
import numpy as np
from matplotlib import pyplot as plt
import cv2
import tensorflow.keras.backend as K
from module.const import *
from module import func, loss

custom_model_path = os.path.join(MODEL_DIR, "full_model.h5")  # tensorflowのモデル
model = tf.lite.Interpreter(model_path="model.tflite")
model = tf.keras.models.load_model(
    custom_model_path, custom_objects={"DiceLoss": loss.DiceLoss}, compile=False
)
model.summary()
imgs = os.listdir("imgs")
for img in imgs:
    img = cv2.imread(os.path.join("imgs", img))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, INPUT_SIZE)
    img = np.array([img]) / 255
    pred = model.predict(img)
    # print(img.shape, pred.shape)
    img = func.draw_line(img[0])
    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.subplot(1, 2, 2)
    plt.imshow(pred[0])
    plt.show()

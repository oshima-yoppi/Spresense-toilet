from typing import Any
import tensorflow as tf
import os
import h5py
import numpy as np
from matplotlib import pyplot as plt
import cv2
import tensorflow.keras.backend as K
from module.const import *
from module import func, loss
import shutil
from tqdm import tqdm

TEST_DIR = "test"
SAVE_DIR = "test_result"
if os.path.exists(SAVE_DIR):
    shutil.rmtree(SAVE_DIR)
os.makedirs(SAVE_DIR)


class TFLitePredictor:
    def __init__(self, model_path):
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def __call__(self, input_data):
        input_data = input_data.astype(np.float32)
        self.interpreter.set_tensor(self.input_details[0]["index"], input_data)
        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(self.output_details[0]["index"])
        return output_data


# print('Quantized model accuracy: ',evaluate_model(interpreter_quant))
interpreter = TFLitePredictor(TFLITE_MODEL_PATH)


imgs = os.listdir(TEST_DIR)
imgs = imgs[::-1]
count = 0
for i, filename in enumerate(tqdm(imgs)):
    img = cv2.imread(os.path.join(TEST_DIR, filename))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    splited_img_lst = func.split_img(img)
    for splited_img in splited_img_lst:
        splited_img = cv2.resize(splited_img, INPUT_SIZE)
        splited_img = np.array([splited_img]) / 255
        pred = interpreter(splited_img)
        splited_img = func.draw_line(splited_img[0])
        splited_img = (splited_img * 255).astype(np.uint8)
        plt.subplot(1, 2, 1)
        plt.imshow(splited_img)
        plt.subplot(1, 2, 2)
        plt.imshow(pred[0])
        save_path = os.path.join(SAVE_DIR, f"{count}.png")
        plt.savefig(save_path)
        plt.close()
        count += 1

    # img = cv2.resize(img, INPUT_SIZE)
    # img_for_plot = img
    # img = np.array([img]) / 255
    # pred = interpreter(img)
    # img = func.draw_line(img[0])
    # img = (img * 255).astype(np.uint8)
    # plt.subplot(1, 2, 1)
    # plt.imshow(img)
    # plt.subplot(1, 2, 2)
    # plt.imshow(pred[0])

    # save_path = os.path.join(SAVE_DIR, f"{i}.png")
    # plt.savefig(save_path)
    # # plt.show()
    # plt.close()

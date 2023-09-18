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


imgs = os.listdir("imgs")
for img in imgs:
    img = cv2.imread(os.path.join("imgs", img))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, INPUT_SIZE)
    img = np.array([img]) / 255
    # x_test.append(img)
    pred = interpreter(img)
    # pred = model.predict(img)
    # print(img.shape, pred.shape)
    img = func.draw_line(img[0])
    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.subplot(1, 2, 2)
    plt.imshow(pred[0])
    plt.show()

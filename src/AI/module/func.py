from module.const import *
import numpy as np


def label_change(label):
    label_output = np.zeros(LABEL_SIZE)
    for i in range(label.shape[0]):
        for j in range(label.shape[1]):
            if label[i, j] == 1:
                label_output[
                    int(i / label.shape[0] * LABEL_SIZE[0]),
                    int(j / label.shape[1] * LABEL_SIZE[1]),
                ] = 1.0

    for i in [0, LABEL_SIZE[0] - 1]:
        for j in range(LABEL_SIZE[1]):
            label_output[i, j] = 0.0
    for j in [0, LABEL_SIZE[1] - 1]:
        for i in range(LABEL_SIZE[0]):
            label_output[i, j] = 0.0
    return label_output

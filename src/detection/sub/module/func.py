import cv2
import numpy as np


def get_diff(base, img):
    dif = base.astype(int) - img.astype(int)
    dif = np.abs(dif)
    dif = dif.astype(np.uint8)
    return dif


def get_diff_mask(dif, th=60):
    dif = np.where(dif > th, 1, 0)
    return dif


class CircleMaching:
    def __init__(self, radius=6):
        self.radius = radius
        self.filter_size = (2 * radius, 2 * radius)  # フィルタのサイズを計算
        self.half_circle_filter = np.zeros(self.filter_size, dtype=np.uint8)
        cv2.ellipse(
            self.half_circle_filter,
            (radius, radius),
            (radius, radius),
            0,
            180,
            360,
            255,
            -1,
        )
        self.half_circle_filter = self.half_circle_filter.astype(np.uint8)

    def get_maching(self, img):
        img = img.astype(np.uint8)
        res = cv2.matchTemplate(img, self.half_circle_filter, cv2.TM_CCOEFF_NORMED)
        return res

    def get_mask(self, res, th=0.5):
        mask = np.where(res > th, 1, 0)
        return mask

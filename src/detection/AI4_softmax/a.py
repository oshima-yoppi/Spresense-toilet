import tensorflow as tf

from tensorflow.keras.applications import MobileNet, MobileNetV2

INPUT_SIZE = (96, 96)
model = MobileNetV2(
    input_shape=(INPUT_SIZE[0], INPUT_SIZE[1], 1),
    include_top=False,
    weights=None,
    alpha=0.35,
)
model.summary()

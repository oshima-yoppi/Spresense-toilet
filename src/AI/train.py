import tensorflow as tf
from keras.layers import Dense, Input, GlobalAveragePooling2D, Dropout, Flatten
from tensorflow.keras.optimizers import Adam
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import CSVLogger
from keras.models import Model
from tensorflow.keras.applications import MobileNet, MobileNetV2
import tensorflow_model_optimization as tfmot


PIX = 98
INPUT_CHANNEL = 3
mobilenet = MobileNetV2(
    input_shape=(PIX, PIX, INPUT_CHANNEL), include_top=False, weights="imagenet"
)
mobilenet.summary()
custom_model = Model(
    inputs=mobilenet.input, outputs=mobilenet.get_layer("block_6_expand_relu").output
)

# 新しいモデルのサマリーを表示
custom_model.summary()
total_params = custom_model.count_params()
print("Total params: ", total_params)
print("Total RAM :", total_params * 4 / 1024 / 1024, "MB")  #

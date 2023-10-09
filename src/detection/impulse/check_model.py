import tensorflow as tf
from tensorflow import keras

model_path = "keras_model/model.h5"
converter = tf.keras.models.load_model(model_path)
converter.summary()

import tensorflow as tf
from tensorflow import keras
from keras.models import Model

model_path = "keras_model/model.h5"
converter = tf.keras.models.load_model(model_path)
converter.summary()
mobile_kcut_model = Model(
    inputs=converter.input, outputs=converter.get_layer("block_6_expand_relu").output
)
mobile_kcut_model.summary()
save_path = "trained_model.h5"
mobile_kcut_model.save(save_path)

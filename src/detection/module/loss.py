import tensorflow as tf
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K


def cross_loss(targets, inputs, class_weights=tf.constant([100.0, 1.0])):
    # クロスエントロピー損失を計算し、クラスごとに重みを適用
    # print(targets.sinputsoutput.shape)
    inputs = tf.cast(inputs, dtype=tf.float32)
    targets = tf.cast(targets, dtype=tf.float32)
    targets = targets[:, :, :, 1]
    inputs = inputs[:, :, :, 1]
    inputs = K.flatten(inputs)
    targets = K.flatten(targets)

    weighted_loss = tf.reduce_mean(
        tf.keras.losses.categorical_crossentropy(targets, inputs) * class_weights
    )
    return weighted_loss


def IoU(targets, inputs, smooth=1e-6):
    batch = len(inputs)
    targets = tf.cast(targets, dtype=tf.float32)
    inputs = tf.cast(inputs, dtype=tf.float32)

    targets = targets[:, :, :, 1]
    inputs = inputs[:, :, :, 1]
    inputs = K.flatten(inputs)
    targets = K.flatten(targets)
    intersection = tf.reduce_sum(inputs * targets)
    iou = (intersection + smooth) / (
        K.sum(targets) + K.sum(inputs) - intersection + smooth
    )
    return iou


def weighted_focal_Loss(targets, inputs, beta=3, smooth=1e-6):
    # targets = targets.astye('float')
    # flatten label and prediction tensors
    # tf_show(inputs[0])
    batch = len(inputs)
    targets = tf.cast(targets, dtype=tf.float32)
    # inputs = K.softmax(inputs, axis=-1)
    # inputs = tf.expand_dims(inputs, axis=-1)
    # inputs = MaxPooling2D(pool_size=(2, 2))(inputs)
    targets = targets[:, :, :, 1]
    inputs = inputs[:, :, :, 1]
    inputs = K.flatten(inputs)
    targets = K.flatten(targets)
    intersection = tf.reduce_sum(inputs * targets)
    precision = intersection / (K.sum(inputs) + smooth)
    recall = intersection / (K.sum(targets) + smooth)
    f = ((1 + beta**2) * precision * recall + smooth) / (
        beta**2 * precision + recall + smooth
    )
    return 1 - f


def DiceLoss(targets, inputs, smooth=1e-6):
    batch = len(inputs)
    targets = tf.cast(targets, dtype=tf.float32)
    # print(inputs.shape, targets.shape)
    # inputs = tf.expand_dims(inputs, axis=-1)
    inputs = inputs[:, :, :, 1]
    targets = targets[:, :, :, 1]
    # print(inputs.shape, targets.shape)
    # inputs = MaxPooling2D(pool_size=(2, 2))(inputs)
    # inputs = K.softmax(inputs, axis=-1)
    inputs = K.flatten(inputs)
    targets = K.flatten(targets)
    # print(inputs.shape, targets.shape)
    intersection = tf.reduce_sum(
        inputs * targets
    )  # https://tensorflow.classcat.com/2018/09/07/tensorflow-tutorials-images-segmentation/
    # print(targets.shape, inputs.shape)
    dice = (2 * intersection + smooth) / (K.sum(targets) + K.sum(inputs) + smooth)
    return 1 - dice

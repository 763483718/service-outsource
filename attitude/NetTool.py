import tensorflow as tf
import numpy as np


def create_weights(shape, stddev=0.05):
    return tf.Variable(tf.truncated_normal(shape, stddev=stddev))


def create_biases(size, value=0.01):  # value 初值
    return tf.Variable(tf.constant(value, shape=[size]))


# 创建一个卷积层 input:传入的矩阵
def create_convolution_layer(input, filter_size, filter_num, use_MaxPool=True, stride_f=1, stride_m=2, ksize=2):
    weights = create_weights(
        shape=[filter_size, filter_size, (int)(input.shape[3]), filter_num])

    biases = create_biases(filter_num)

    layer = tf.nn.conv2d(input, weights, strides=[
                         1, stride_f, stride_f, 1], padding='SAME')
    layer += biases
    layer = tf.nn.relu(layer)

    if use_MaxPool:
        layer = tf.nn.max_pool(layer, ksize=[1, 2, 2, 1], strides=[
            1, stride_m, stride_m, 1], padding='SAME')

    return layer


def create_flatten_layer(input):  # 将图片伸展开
    layer_shape = input.get_shape()
    feature_num = layer_shape[1:4].num_elements()

    layer = tf.reshape(input, shape=[-1, feature_num])
    return layer


def create_fc_layer(input, weights_shape, keep_prob, use_relu=True):  # 创建一个全链接层
    weights = create_weights(weights_shape)
    biases = create_biases(weights_shape[1])
    layer = tf.matmul(input, weights) + biases
    layer = tf.nn.dropout(layer, keep_prob)

    if use_relu:
        layer = tf.nn.relu(layer)
    return layer

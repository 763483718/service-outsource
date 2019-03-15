import tensorflow as tf
import numpy as np


def create_weights(shape, stddev=0.05):
    return tf.Variable(tf.truncated_normal(shape, stddev=stddev))


def create_biases(size, value=0.01):  # value 初值
    return tf.Variable(tf.constant(value, shape=[size]))


def create_convolution_layer(input, filter_size, filter_num):  # 创建一个卷积层 input:传入的矩阵
    weights = create_weights(
        shape=[filter_size, filter_size, (int)(input.shape[3]), filter_num])

    biases = create_biases(filter_num)

    layer = tf.nn.conv2d(input, weights, strides=[1, 1, 1, 1], padding='SAME')
    layer += biases
    layer = tf.nn.relu(layer)

    layer = tf.nn.max_pool(layer, ksize=[1, 2, 2, 1], strides=[
                           1, 2, 2, 1], padding='SAME')
    return layer


def create_flatten_layer(input):  # 将图片伸展开
    layer_shape = input.get_shape()
    feature_num = layer_shape[1:4].num_elements()

    layer = tf.reshape(input, shape=[-1, feature_num])
    return layer


# size是将边长分为几份 [[4,3],[2,4]]
def create_spp_layer(input, sizes):
    # shape = input.get_shape().as_list()
    shape = tf.shape(input,'tf.int32')
    w = shape[1]
    h = shape[2]

    spp_layer = None
    for size in sizes:
        # test = np.ceil(height/(int)(size[0]))
        ksize = [1, np.ceil(w/size[0]),
                 np.ceil(h/size[1]), 1]
        strides = [1, np.floor(width/size[0]).astype(np.int32),
                   np.floor(height/size[1].astype(np.int32)), 1]
        layer = tf.nn.max_pool(
            input, ksize=ksize, strides=strides, padding='SAME')
        layer = tf.reshape(layer, (shape[0], -1))

        if spp_layer == None:
            spp_layer = tf.reshape(layer, (shape[0], -1))
        else:
            spp_layer = tf.concat((pool, layer), 1)
    return spp_layer


def create_fc_layer(input, weights_shape, keep_prob, use_relu=True):  # 创建一个全链接层
    weights = create_weights(weights_shape)
    biases = create_biases(weights_shape[1])
    layer = tf.matmul(input, weights) + biases
    layer = tf.nn.dropout(layer, keep_prob)

    if use_relu:
        layer = tf.nn.relu(layer)
    return layer


def test():

    data = np.ones(shape=[1, 11, 13, 3])
    x = tf.placeholder(dtype='float', shape=[None, None, None, None], name='X')
    width = tf.placeholder(dtype='int32', shape=[1], name='width')
    height = tf.placeholder(dtype='int32', shape=[1], name='height')
    sizes = [[1, 1], [2, 2]]
    spp_net = create_spp_layer(x, sizes)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        spp = sess.run(spp_net, feed_dict={x: data})
        print(spp)

test()
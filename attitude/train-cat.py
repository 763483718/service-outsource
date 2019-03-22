import dataset
import tensorflow as tf
import numpy as np
import cv2 as cv

imageSize = 64
channels = 3
batchSize = 32
class_num = 2

filter1_size = 3
filter1_num = 32

filter2_size = 3
filter2_num = 32

filter3_size = 3
filter3_num = 64

layer_fc_size = 1024

keep_prob = 0.7
# create a weights in shape
# [in] shape: the shape of the weights
# [out] a weights in the shape


def create_weights(shape):
    return tf.Variable(tf.truncated_normal(shape, stddev=0.05))

# create a biases in size


def create_biases(size):
    return tf.Variable(tf.constant(0.01, shape=[size]))


def create_convolution_layer(input, filter_size, filter_num):
    weights = create_weights(
        shape=[filter_size, filter_size, (int)(input.shape[3]), filter_num])

    biases = create_biases(filter_num)

    layer = tf.nn.conv2d(input, weights, strides=[1, 1, 1, 1], padding='SAME')
    layer += biases
    layer = tf.nn.relu(layer)

    layer = tf.nn.max_pool(layer, ksize=[1, 2, 2, 1], strides=[
                           1, 2, 2, 1], padding='SAME')
    return layer


def create_flatten_layer(input):
    layer_shape = input.get_shape()
    feature_num = layer_shape[1:4].num_elements()

    layer = tf.reshape(input, shape=[-1, feature_num])
    return layer


def create_fc_layer(input, weights_shape, keep_prob, use_relu=True):
    weights = create_weights(weights_shape)
    biases = create_biases(weights_shape[1])
    layer = tf.matmul(input, weights) + biases
    layer = tf.nn.dropout(layer, keep_prob)

    if use_relu:
        layer = tf.nn.relu(layer)
    return layer


def main(times):
    X = tf.placeholder('float', shape=[
                       None, imageSize, imageSize, channels],name='X')
    Y = tf.placeholder('float', shape=[None, class_num], name='Y')

    convolution_layer1 = create_convolution_layer(X, filter1_size, filter1_num)
    convolution_layer2 = create_convolution_layer(
        convolution_layer1, filter2_size, filter2_num)
    convolution_layer3 = create_convolution_layer(
        convolution_layer2, filter3_size, filter3_num)

    flatten_layer = create_flatten_layer(convolution_layer3)

    # layer_shape = flatten_layer.get_shape()
    # fc_input_size = layer_shape[1:4].num_elements()

    fc_input_size = flatten_layer.get_shape()[1:4].num_elements()

    fc_layer = create_fc_layer(
        flatten_layer, [fc_input_size, layer_fc_size], keep_prob)
    out_layer = create_fc_layer(
        fc_layer, [layer_fc_size, class_num], keep_prob, use_relu=False)

    pred_Y = tf.nn.softmax(out_layer, name='pred_Y')

    loss = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(labels=Y, logits=pred_Y))
    optimizer = tf.train.AdamOptimizer().minimize(loss)  # learning_rate=0.0001

    temp = tf.equal(tf.arg_max(pred_Y, 1), tf.arg_max(Y, 1))
    accuracy = tf.reduce_mean(tf.cast(temp, tf.float32))

    filePath = '/Mycomputer/pythonCode/tensorflow/深度学习框架Tensorflow案例实战视频课程【195107】Tensorflow简介与安装/猫狗识别/training_data'
    filePath_test = '/Mycomputer/pythonCode/tensorflow/深度学习框架Tensorflow案例实战视频课程【195107】Tensorflow简介与安装/猫狗识别/testing_data'
    classes = ['cats', 'dogs']

    trainSet = dataset.dataSet(filePath, imageSize, classes)
    testSet = dataset.dataSet(filePath_test, imageSize, classes)
    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        for i in range(times+1):
            batchX, batchY, _ = trainSet.next_batch(batchSize)
            sess.run([optimizer], feed_dict={X: batchX, Y: batchY})

            # for i in range(batchSize):
            #     img = batchX[i]
            #     # cc = c[i]
            #     cc = batchY[i]
            #     cv.imshow(str(cc),img)
            #     cv.waitKey()

            if i % 25 == 0:
                _, train_ac = sess.run([optimizer, accuracy], feed_dict={
                                       X: batchX, Y: batchY})
                batchX, batchY, _ = testSet.next_batch(batchSize)
                a, _ = sess.run([accuracy, optimizer],
                                feed_dict={X: batchX, Y: batchY})
                print(i, '\ttrain_accuracy:\t',
                      train_ac, '\ttest_accuracy:\t', a)
                if i % 1000 == 0 and i != 0:
                    saver.save(sess, './dogs-cats-model/dog-cat.ckpt',
                               global_step=i)


main(10000)

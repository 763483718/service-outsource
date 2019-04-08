
'''
    由于训练模型的大小超过了组委会对提交材料的要求，所以没有办法提交模型。

    所以提交模型构建代码
'''
import tensorflow as tf
import numpy as np
import dataset
import NetTool
import random
import parameter

filePath = ['/Volumes/Seagate Backup Plus Drive/服务外包/picture/tset/1']
txtPath = ['/Volumes/Seagate Backup Plus Drive/服务外包/picture/tset/body']

classes = ['right_sleep', 'right_play_telephone', 'right_study',
           'left_sleep', 'left_play_telephone', 'left_study',
           'center_sleep', 'center_play_telephone', 'center_study']
class_num = 3

imgSize = parameter.imgSize
X = tf.placeholder('float', shape=[None, imgSize, imgSize, 3], name='X')
Y = tf.placeholder('float', shape=[None,  class_num], name='Y')

filter1_size = 7
filter1_num = 64

filter2_size = 1
filter2_num = 64

filter3_size = 3
filter3_num = 192

filter1x1_size = 1


conv_layer1 = NetTool.create_convolution_layer(  # 7x7 64 2    3x3 64 2
    X, filter1_size, filter1_num, stride_f=2, ksize=3, stride_m=2)

conv_layer2 = NetTool.create_convolution_layer(  # 1x1 64 1
    conv_layer1, filter2_size, filter2_num, use_MaxPool=False)

conv_layer3 = NetTool.create_convolution_layer(  # 3x3 192 1  3x3 192 1
    conv_layer2, filter3_size, filter3_num, stride_f=1, stride_m=2, ksize=3)

# inception1
########################################################################
inception1_conv_a = NetTool.create_convolution_layer(
    conv_layer3, filter1x1_size, 64, use_MaxPool=False, stride_f=1)

inception1_conv_b = NetTool.create_convolution_layer(
    conv_layer3, filter1x1_size, 96, use_MaxPool=False, stride_f=1)
inception1_conv_b = NetTool.create_convolution_layer(
    inception1_conv_b, 3, 128, use_MaxPool=False, stride_f=1)

inception1_conv_c = NetTool.create_convolution_layer(
    conv_layer3, filter1x1_size, 16, use_MaxPool=False, stride_f=1)
inception1_conv_c = NetTool.create_convolution_layer(
    inception1_conv_c, 5, 32, use_MaxPool=False, stride_f=1)

inception1_conv_d = tf.nn.max_pool(conv_layer3, ksize=[1, 3, 3, 1], strides=[
                                   1, 1, 1, 1], padding='SAME')
inception1_conv_d = NetTool.create_convolution_layer(
    inception1_conv_d, 1, 32, stride_f=1, use_MaxPool=False)

inception1_concat = tf.concat([inception1_conv_a, inception1_conv_b,
                               inception1_conv_c, inception1_conv_d], 3, name='concat1')
#######################################################################

# inception2
#######################################################################
inception2_conv_a = NetTool.create_convolution_layer(
    inception1_concat, filter1x1_size, 128, use_MaxPool=False, stride_f=1)

inception2_conv_b = NetTool.create_convolution_layer(
    inception1_concat, filter1x1_size, 128, use_MaxPool=False, stride_f=1)
inception2_conv_b = NetTool.create_convolution_layer(
    inception2_conv_b, 3, 192, use_MaxPool=False, stride_f=1)

inception2_conv_c = NetTool.create_convolution_layer(
    inception1_concat, filter1x1_size, 32, use_MaxPool=False, stride_f=1)
inception2_conv_c = NetTool.create_convolution_layer(
    inception2_conv_c, 5, 96, use_MaxPool=False, stride_f=1)

inception2_conv_d = tf.nn.max_pool(inception1_concat, ksize=[1, 3, 3, 1], strides=[
                                   1, 1, 1, 1], padding='SAME')
inception2_conv_d = NetTool.create_convolution_layer(
    inception2_conv_d, 1, 64, stride_f=1, use_MaxPool=False)

inception2_concat = tf.concat([inception2_conv_a, inception2_conv_b,
                               inception2_conv_c, inception2_conv_d], 3, name='concat2')

inception2_concat = tf.nn.max_pool(inception2_concat, ksize=[
                                   1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME')
#######################################################################

# inception3
#######################################################################
inception3_conv_a = NetTool.create_convolution_layer(
    inception2_concat, filter1x1_size, 192, use_MaxPool=False, stride_f=1)

inception3_conv_b = NetTool.create_convolution_layer(
    inception2_concat, filter1x1_size, 96, use_MaxPool=False, stride_f=1)
inception3_conv_b = NetTool.create_convolution_layer(
    inception3_conv_b, 3, 208, use_MaxPool=False, stride_f=1)

inception3_conv_c = NetTool.create_convolution_layer(
    inception2_concat, filter1x1_size, 16, use_MaxPool=False, stride_f=1)
inception3_conv_c = NetTool.create_convolution_layer(
    inception3_conv_c, 5, 48, use_MaxPool=False, stride_f=1)

inception3_conv_d = tf.nn.max_pool(inception2_concat, ksize=[1, 3, 3, 1], strides=[
                                   1, 1, 1, 1], padding='SAME')
inception3_conv_d = NetTool.create_convolution_layer(
    inception3_conv_d, 1, 64, stride_f=1, use_MaxPool=False)

inception3_concat = tf.concat([inception3_conv_a, inception3_conv_b,
                               inception3_conv_c, inception3_conv_d], 3, name='concat3')
#######################################################################

# inception4
#######################################################################
inception4_conv_a = NetTool.create_convolution_layer(
    inception3_concat, filter1x1_size, 160, use_MaxPool=False, stride_f=1)

inception4_conv_b = NetTool.create_convolution_layer(
    inception3_concat, filter1x1_size, 112, use_MaxPool=False, stride_f=1)
inception4_conv_b = NetTool.create_convolution_layer(
    inception4_conv_b, 3, 224, use_MaxPool=False, stride_f=1)

inception4_conv_c = NetTool.create_convolution_layer(
    inception3_concat, filter1x1_size, 24, use_MaxPool=False, stride_f=1)
inception4_conv_c = NetTool.create_convolution_layer(
    inception4_conv_c, 5, 64, use_MaxPool=False, stride_f=1)

inception4_conv_d = tf.nn.max_pool(inception3_concat, ksize=[1, 3, 3, 1], strides=[
                                   1, 1, 1, 1], padding='SAME')
inception4_conv_d = NetTool.create_convolution_layer(
    inception4_conv_d, 1, 64, stride_f=1, use_MaxPool=False)

inception4_concat = tf.concat([inception4_conv_a, inception4_conv_b,
                               inception4_conv_c, inception4_conv_d], 3, name='concat4')
#######################################################################

# inception5
#######################################################################
inception5_conv_a = NetTool.create_convolution_layer(
    inception4_concat, filter1x1_size, 128, use_MaxPool=False, stride_f=1)

inception5_conv_b = NetTool.create_convolution_layer(
    inception4_concat, filter1x1_size, 128, use_MaxPool=False, stride_f=1)
inception5_conv_b = NetTool.create_convolution_layer(
    inception5_conv_b, 3, 256, use_MaxPool=False, stride_f=1)

inception5_conv_c = NetTool.create_convolution_layer(
    inception4_concat, filter1x1_size, 24, use_MaxPool=False, stride_f=1)
inception5_conv_c = NetTool.create_convolution_layer(
    inception5_conv_c, 5, 64, use_MaxPool=False, stride_f=1)

inception5_conv_d = tf.nn.max_pool(inception4_concat, ksize=[1, 3, 3, 1], strides=[
                                   1, 1, 1, 1], padding='SAME')
inception5_conv_d = NetTool.create_convolution_layer(
    inception5_conv_d, 1, 64, stride_f=1, use_MaxPool=False)

inception5_concat = tf.concat([inception5_conv_a, inception5_conv_b,
                               inception5_conv_c, inception5_conv_d], 3, name='concat5')
#######################################################################

# inception6
#######################################################################
inception6_conv_a = NetTool.create_convolution_layer(
    inception5_concat, filter1x1_size, 112, use_MaxPool=False, stride_f=1)

inception6_conv_b = NetTool.create_convolution_layer(
    inception5_concat, filter1x1_size, 144, use_MaxPool=False, stride_f=1)
inception6_conv_b = NetTool.create_convolution_layer(
    inception6_conv_b, 3, 288, use_MaxPool=False, stride_f=1)

inception6_conv_c = NetTool.create_convolution_layer(
    inception5_concat, filter1x1_size, 32, use_MaxPool=False, stride_f=1)
inception6_conv_c = NetTool.create_convolution_layer(
    inception6_conv_c, 5, 64, use_MaxPool=False, stride_f=1)

inception6_conv_d = tf.nn.max_pool(inception5_concat, ksize=[1, 3, 3, 1], strides=[
                                   1, 1, 1, 1], padding='SAME')
inception6_conv_d = NetTool.create_convolution_layer(
    inception6_conv_d, 1, 64, stride_f=1, use_MaxPool=False)

inception6_concat = tf.concat([inception6_conv_a, inception6_conv_b,
                               inception6_conv_c, inception6_conv_d], 3, name='concat6')
#######################################################################

# inception7
#######################################################################
inception7_conv_a = NetTool.create_convolution_layer(
    inception6_concat, filter1x1_size, 256, use_MaxPool=False, stride_f=1)

inception7_conv_b = NetTool.create_convolution_layer(
    inception6_concat, filter1x1_size, 160, use_MaxPool=False, stride_f=1)
inception7_conv_b = NetTool.create_convolution_layer(
    inception7_conv_b, 3, 320, use_MaxPool=False, stride_f=1)

inception7_conv_c = NetTool.create_convolution_layer(
    inception6_concat, filter1x1_size, 32, use_MaxPool=False, stride_f=1)
inception7_conv_c = NetTool.create_convolution_layer(
    inception7_conv_c, 5, 128, use_MaxPool=False, stride_f=1)

inception7_conv_d = tf.nn.max_pool(inception6_concat, ksize=[1, 3, 3, 1], strides=[
                                   1, 1, 1, 1], padding='SAME')
inception7_conv_d = NetTool.create_convolution_layer(
    inception7_conv_d, 1, 128, stride_f=1, use_MaxPool=False)

inception7_concat = tf.concat([inception7_conv_a, inception7_conv_b,
                               inception7_conv_c, inception7_conv_d], 3, name='concat7')

inception7_concat = tf.nn.max_pool(inception7_concat, ksize=[
                                   1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME')
#######################################################################

# inception8
#######################################################################
inception8_conv_a = NetTool.create_convolution_layer(
    inception7_concat, filter1x1_size, 256, use_MaxPool=False, stride_f=1)

inception8_conv_b = NetTool.create_convolution_layer(
    inception7_concat, filter1x1_size, 160, use_MaxPool=False, stride_f=1)
inception8_conv_b = NetTool.create_convolution_layer(
    inception8_conv_b, 3, 320, use_MaxPool=False, stride_f=1)

inception8_conv_c = NetTool.create_convolution_layer(
    inception7_concat, filter1x1_size, 32, use_MaxPool=False, stride_f=1)
inception8_conv_c = NetTool.create_convolution_layer(
    inception8_conv_c, 5, 128, use_MaxPool=False, stride_f=1)

inception8_conv_d = tf.nn.max_pool(inception7_concat, ksize=[1, 3, 3, 1], strides=[
                                   1, 1, 1, 1], padding='SAME')
inception8_conv_d = NetTool.create_convolution_layer(
    inception8_conv_d, 1, 128, stride_f=1, use_MaxPool=False)

inception8_concat = tf.concat([inception8_conv_a, inception8_conv_b,
                               inception8_conv_c, inception8_conv_d], 3, name='concat8')
#######################################################################

# inception9
#######################################################################
inception9_conv_a = NetTool.create_convolution_layer(
    inception8_concat, filter1x1_size, 384, use_MaxPool=False, stride_f=1)

inception9_conv_b = NetTool.create_convolution_layer(
    inception8_concat, filter1x1_size, 192, use_MaxPool=False, stride_f=1)
inception9_conv_b = NetTool.create_convolution_layer(
    inception9_conv_b, 3, 384, use_MaxPool=False, stride_f=1)

inception9_conv_c = NetTool.create_convolution_layer(
    inception8_concat, filter1x1_size, 48, use_MaxPool=False, stride_f=1)
inception9_conv_c = NetTool.create_convolution_layer(
    inception9_conv_c, 5, 128, use_MaxPool=False, stride_f=1)

inception9_conv_d = tf.nn.max_pool(inception8_concat, ksize=[1, 3, 3, 1], strides=[
                                   1, 1, 1, 1], padding='SAME')
inception9_conv_d = NetTool.create_convolution_layer(
    inception9_conv_d, 1, 128, stride_f=1, use_MaxPool=False)

inception9_concat = tf.concat([inception9_conv_a, inception9_conv_b,
                               inception9_conv_c, inception9_conv_d], 3, name='concat9')

inception9_concat = tf.nn.avg_pool(inception9_concat, ksize=[
                                   1, 7, 7, 1], strides=[1, 1, 1, 1], padding='SAME')
#######################################################################

# Fully Connected
#######################################################################
flatten_layer = NetTool.create_flatten_layer(inception9_concat)
fc_input_size = flatten_layer.get_shape()[1:4].num_elements()
fc_layer = NetTool.create_fc_layer(flatten_layer, [fc_input_size, 1000], 0.4)
out_layer = NetTool.create_fc_layer(fc_layer, [1000, 3], 0.4, use_relu=False)

pred_Y = tf.nn.softmax(out_layer, name='pred_Y')

loss = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=Y, logits=pred_Y))
optimizer = tf.train.AdamOptimizer().minimize(loss)  # learning_rate=0.0001

temp = tf.equal(tf.arg_max(pred_Y, 1), tf.arg_max(Y, 1))
accuracy = tf.reduce_mean(tf.cast(temp, tf.float32))


print('开始加载训练数据集')
trainSet = dataset.dataSet(filePath, classes, way='txt', txtPath=txtPath)
print('开始加载测试数据集')
txtFilePath = '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-05/body1'
testSet = dataset.dataSet(txtFilePath, classes, way='image')
print('数据集加载完成')

saver = tf.train.Saver()
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    for i in range(10001):
        batchX, batchY, _ = trainSet.next_batch(32)
        sess.run(optimizer, feed_dict={X: batchX, Y: batchY})
        if i % 25 == 0:
            _, train_ac = sess.run([optimizer, accuracy], feed_dict={
                X: batchX, Y: batchY})
            batchX, batchY, _ = testSet.next_batch(5)
            a, _ = sess.run([accuracy, optimizer],
                            feed_dict={X: batchX, Y: batchY})
            print(i, '\ttrain_accuracy:\t',
                  train_ac, '\ttest_accuracy:\t', a)
            if i % 1000 == 0 and i != 0:
                saver.save(sess, './model/body.ckpt',
                           global_step=i)

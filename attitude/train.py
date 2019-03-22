import dataset
import tensorflow as tf
import numpy as np
import cv2 as cv
import NetTool
import parameter

filePath = ['/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-05/2',
            # '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2018-12-27/1',
            # '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2018-12-27/2',
            # '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2018-12-27/3',
            # '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-17/1',
            # '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-17/2',
            # '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-05/修改间隔后/4',
            # '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-05/修改间隔后/5'
            ]

txtPath = ['/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-05/body2',
        #    '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2018-12-27/body1',
        #    '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2018-12-27/body2',
        #    '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2018-12-27/body3',
        #    '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-17/body1',
        #    '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-17/body2',
        #    '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-05/修改间隔后/body4',
        #    '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-05/修改间隔后/body5'
           ]


classes = ['right_sleep', 'right_play_telephone', 'right_study',
           'left_sleep', 'left_play_telephone', 'left_study',
           'center_sleep', 'center_play_telephone', 'center_study']


imgSize = parameter.imgSize
class_num = 3

filter1_size = 5
filter1_num = 16

filter2_size = 5
filter2_num = 64

filter3_size = 5
filter3_num = 128

fc_size = 1024
keep_prob = 0.7
batchSize = 64

X = tf.placeholder('float', shape=[None, imgSize, imgSize, 3], name='X')
Y = tf.placeholder('float', shape=[
    None,  class_num], name='Y')

convolution_layer1 = NetTool.create_convolution_layer(
    X, filter1_size, filter1_num)
convolution_layer2 = NetTool.create_convolution_layer(
    convolution_layer1, filter2_size, filter2_num)
convolution_layer3 = NetTool.create_convolution_layer(
    convolution_layer2, filter3_size, filter3_num)

flatten_layer = NetTool.create_flatten_layer(convolution_layer3)

fc_input_size = flatten_layer.get_shape()[1:4].num_elements()

fc_layer = NetTool.create_fc_layer(
    flatten_layer, [fc_input_size, fc_size], keep_prob)
out_layer = NetTool.create_fc_layer(
    fc_layer, [fc_size, class_num], keep_prob, use_relu=False)

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
        batchX, batchY, _ = trainSet.next_batch(batchSize)
        # print(type(batchX))
        sess.run([optimizer], feed_dict={X: batchX, Y: batchY})
        if i % 25 == 0:
            _, train_ac = sess.run([optimizer, accuracy], feed_dict={
                X: batchX, Y: batchY})
            batchX, batchY, _ = testSet.next_batch(batchSize)
            a, _ = sess.run([accuracy, optimizer],
                            feed_dict={X: batchX, Y: batchY})
            print(i, '\ttrain_accuracy:\t',
                  train_ac, '\ttest_accuracy:\t', a)
            if i % 1000 == 0 and i != 0:
                saver.save(sess, './model/body.ckpt',
                           global_step=i)

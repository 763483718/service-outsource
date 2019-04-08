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

filter1_size = 3
filter1_num = 64

filter2_size = 3
filter2_num = 64

filter3_size = 3
filter3_num = 128

filter4_size = 3
filter4_num = 128

filter5_size = 3
filter5_num = 256

filter6_size = 3
filter6_num = 256

filter7_size = 1
filter7_num = 256

filter8_size = 3
filter8_num = 512

filter9_size = 3
filter9_num = 512

filter10_size = 1
filter10_num = 512

filter11_size = 3
filter11_num = 512

filter12_size = 3
filter12_num = 512

filter13_size = 1
filter13_num = 512

fc1_size = 4096
fc2_size = 4096
fc3_size = 1000

keep_prob = 0.7
batchSize = 64

X = tf.placeholder('float', shape=[None, imgSize, imgSize, 3], name='X')
Y = tf.placeholder('float', shape=[
    None,  class_num], name='Y')


convolution_layer1 = NetTool.create_convolution_layer(
    X, filter1_size, filter1_num)
convolution_layer2 = NetTool.create_convolution_layer(
    convolution_layer1, filter2_size, filter2_num, True)


convolution_layer3 = NetTool.create_convolution_layer(
    convolution_layer2, filter3_size, filter3_num)
convolution_layer4 = NetTool.create_convolution_layer(
    convolution_layer3, filter4_size, filter4_num, True)


convolution_layer5 = NetTool.create_convolution_layer(
    convolution_layer4, filter5_size, filter5_num)
convolution_layer6 = NetTool.create_convolution_layer(
    convolution_layer5, filter6_size, filter6_num)
convolution_layer7 = NetTool.create_convolution_layer(
    convolution_layer6, filter7_size, filter7_num, True)


convolution_layer8 = NetTool.create_convolution_layer(
    convolution_layer7, filter8_size, filter8_num)
convolution_layer9 = NetTool.create_convolution_layer(
    convolution_layer8, filter9_size, filter9_num)
convolution_layer10 = NetTool.create_convolution_layer(
    convolution_layer9, filter10_size, filter10_num, True)


convolution_layer11 = NetTool.create_convolution_layer(
    convolution_layer10, filter11_size, filter11_num)
convolution_layer12 = NetTool.create_convolution_layer(
    convolution_layer11, filter12_size, filter12_num)
convolution_layer13 = NetTool.create_convolution_layer(
    convolution_layer12, filter13_size, filter13_num, True)


flatten_layer = NetTool.create_flatten_layer(convolution_layer13)

fc1_input_size = flatten_layer.get_shape()[1:4].num_elements()
fc1_layer = NetTool.create_fc_layer(
    flatten_layer, [fc1_input_size, fc1_size], keep_prob)

fc2_input_size = fc1_layer.get_shape()[1:4].num_elements()
fc2_layer = NetTool.create_fc_layer(
    fc1_layer, [fc2_input_size, fc2_size], keep_prob)

fc3_input_size = fc2_layer.get_shape()[1:4].num_elements()
fc3_layer = NetTool.create_fc_layer(
    fc2_layer, [fc3_input_size, fc3_size], keep_prob)

out_layer = NetTool.create_fc_layer(
    fc3_layer, [fc3_size, class_num], keep_prob, use_relu=False)

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

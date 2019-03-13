import tensorflow as tf
import numpy as np
import cv2 as cv
import glob

imageSize = 64
channels = 3


class Predict():
    def __init__(self, path_session=None, imageSize=64, channels=3, classes=None):
        self._path_session = path_session
        self._imageSize = imageSize
        self._channels = channels
        self._cls = classes
        # self._images = []

    def set_config(self, path_session=None, imageSize=None, channels=None, classes=None):
        if path_session != None:
            self._path_session = path_session
        if imageSize != None:
            self._imageSize = imageSize
        if channels != None:
            self._channels = channels
        if classes != None:
            self._cls = classes

    def predict(self, paths=None, images=None):
        if paths == None and images == None:
            return
        imgs = []
        if images == None:
            for path in paths:
                print(path)
                img = cv.imread(path)
                img = cv.resize(
                    img, (self._imageSize, self._imageSize), 0, 0, cv.INTER_LINEAR)
                img = img.astype(np.float32)
                img = np.multiply(img, 1.0 / 255.0)
                imgs.append(img)
            imgs = np.array(imgs)

        with tf.Session() as sess:
            # Step-1: Recreate the network graph. At this step only graph is created.
            saver = tf.train.import_meta_graph(
                './dogs-cats-model/dog-cat.ckpt-10000.meta')
            # Step-2: Now let's load the weights saved using the restore method.
            saver.restore(sess, './dogs-cats-model/dog-cat.ckpt-10000')

            # Accessing the default graph which we have restored
            graph = tf.get_default_graph()

            # Now, let's get hold of the op that we can be processed to get the output.
            # In the original network y_pred is the tensor that is the prediction of the network
            pred_Y = graph.get_tensor_by_name("pred_Y:0")

            # Let's feed the images to the input placeholders
            X = graph.get_tensor_by_name("X:0")
            Y = graph.get_tensor_by_name("Y:0")
            y = np.zeros(shape=[len(imgs), len(self._cls)])

            pred = sess.run(pred_Y, feed_dict={X: imgs, Y: y})
            
            for i in pred:
                print(self._cls[i.argmax()])


def main():

    filePath = '/Mycomputer/pythonCode/tensorflow/深度学习框架Tensorflow案例实战视频课程【195107】Tensorflow简介与安装/猫狗识别/**.jpg'
    files = glob.glob(filePath)

    predict = Predict(classes=['cats', 'dogs'])
    predict.predict(paths=files)


main()

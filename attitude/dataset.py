import cv2 as cv
import glob
from sklearn.utils import shuffle
import numpy as np


def cutImage(img, x, y, w, h):
    return img[y:y+h, x:x+w]


class dataSet(object):
    def __init__(self, filePath, imgSize, classess, txtPath=None, bodyPos=None):  # bodyPos指左中右
        self._filePath = filePath
        self._imgSize = imgSize
        self._classess = classess
        self._txtPath = txtPath
        self._bodyPos = bodyPos

        self._images = []
        self._labels = []
        self._cls = []
        self._pointer = 0

        # self.loadImage()
        self.loadImageByTXT()
        # self.loadImageByTXT(
        #     '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-05/body2', '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-05/2')
        self._dataSetSize = self._images.shape[0]
        print(self._dataSetSize)
        sleepCount = 0
        telephoneCount = 0
        studyCount = 0
        for i in self._labels:
            if i == 3:
                sleepCount += 1
            elif i == 4:
                telephoneCount += 1
            else:
                studyCount += 1
        print(sleepCount, telephoneCount, studyCount)

        # print(self._labels)
        # print(self._cls.shape)

    @property
    def images(self):
        return self._images

    @property
    def labels(self):
        return self._labels

    @property
    def cls(self):
        return self._cls

    def loadImageByTXT(self):
        for i in range(len(self._txtPath)):
            path = self._txtPath[i] + '/**.txt'
            paths = glob.glob(path)
            for txtPath in paths:
                pos1 = txtPath.rfind('/')
                pos2 = txtPath.rfind('.')
                num = txtPath[pos1+1:pos2]
                imgPath = self._filePath[i] + '/' + str(num) + '.jpg'
                f = open(txtPath, 'r')
                img = cv.imread(imgPath)
                shape = img.shape
                img = cv.resize(img, ((int)(shape[1]/2), (int)
                                      (shape[0]/2)), interpolation=cv.INTER_LINEAR)
                lines = f.readlines()
                cv.imshow('img', img)
                for line in lines:
                    line_dict = eval(line)
                    if self._bodyPos != None:
                        if line_dict['status'][0] != self._bodyPos:
                            continue
                    cut_img = cutImage(
                        img, line_dict['left'], line_dict['top'], line_dict['width'], line_dict['height'])
                    self._images.append(cut_img)
                    self._labels.append(
                        self._classess.index(line_dict['status']))
                    # cv.imshow(str(line_dict['status']), cut_img)
                    # cv.waitKey()
                del img
        self._images = np.array(self._images)
        self._labels = np.array(self._labels)

    def loadImage(self, filePath=None):
        if filePath != None:
            self._filePath = filePath
        for file in self._classess:
            path = self._filePath + '/' + file + '/**.jpg'
            files = glob.glob(path)
            index = self._classess.index(file)
            label = np.zeros(len(self._classess))
            label[index] = 1.0

            for imgPath in files:
                img = cv.imread(imgPath)
                img = cv.resize(
                    img, (self._imgSize, self._imgSize), 0, 0, cv.INTER_LINEAR)
                img = img.astype(np.float32)
                img = np.multiply(img, 1.0 / 255.0)

                self._images.append(img)
                self._labels.append(label)
                self._cls.append(file)
        self._images = np.array(self._images)
        self._labels = np.array(self._labels)
        self._cls = np.array(self._cls)
        self._images, self._labels, self._cls = shuffle(
            self._images, self._labels, self._cls)
        # for i in range(1000):
        #     img = self._images[i]
        #     lab = self._labels[i]
        #     c = self._cls[i]
        #     # img = list(img)
        #     cv.imshow(str(c), img)
        #     cv.waitKey()

    def next_batch(self, batchSize):
        end = self._pointer + batchSize
        if end > self._dataSetSize:
            assert batchSize <= self._dataSetSize
            end %= self._dataSetSize
            start = self._pointer
            imgA = self._images[start:]
            imgB = self._images[0:end]
            labelA = self.labels[start:]
            labelB = self.labels[0:end]
            clsA = self._cls[start:]
            clsB = self.cls[0:end]
            self._pointer = end
            # print(clsA.shape, clsB.shape, '\n\n\n')
            classes = np.hstack((clsA, clsB))
            labels = np.vstack((labelA, labelB))
            images = np.vstack((imgA, imgB))

            return images, labels, classes
        start = self._pointer
        self._pointer = end
        return self._images[start:end], self._labels[start:end], self._cls[start:end]


# filePath = '/Mycomputer/pythonCode/tensorflow/深度学习框架Tensorflow案例实战视频课程【195107】Tensorflow简介与安装/猫狗识别/training_data'

filePath = ['/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-05/2',
            '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2018-12-27/1',
            '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2018-12-27/2',
            '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2018-12-27/3']
txtPath = ['/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-05/body2',
           '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2018-12-27/body1',
           '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2018-12-27/body2',
           '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2018-12-27/body3']


classes = ['right_sleep', 'right_play_telephone', 'right_study',
           'left_sleep', 'left_play_telephone', 'left_study',
           'center_sleep', 'center_play_telephone', 'center_study']
dataSetT = dataSet(filePath, 256, classes, txtPath=txtPath, bodyPos='r')
# imgs, labels, classess = dataSetT.next_batch(48)

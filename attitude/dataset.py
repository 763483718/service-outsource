import cv2 as cv
import glob
# from sklearn.utils import shuffle
import random
import numpy as np
import parameter


def cutImage(img, x, y, w, h):
    return img[y:y+h, x:x+w]


class dataSet(object):
    def __init__(self, filePath,  classess, way, imgSize=parameter.imgSize, txtPath=None, bodyPos=None):  # bodyPos指左中右
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
        if way == 'txt':
            self.loadImageByTXT()
        elif way == 'image':
            self.loadImage()

        temp = list(zip(self._images, self._labels))
        random.shuffle(temp)
        self._images[:], self._labels[:] = zip(*temp)
        self._images = np.array(self._images)
        self._labels = np.array(self._labels)
        shape = self._images.shape
        self._dataSetSize = self._images.shape[0]
        print(self._dataSetSize)

    def Expansion(self, img, label, size=None, pan=10, expansion=1):  # expansion 是否扩展
        if size == None:
            size = self._imgSize
        black_img = np.zeros(
            size*size*3, dtype=np.uint8).reshape(size, size, 3)
        shape = img.shape
        bigger = max(shape[0], shape[1])
        if bigger > 200:
            ratio = 200/bigger
            img = cv.resize(
                img, ((int)(shape[1]*ratio), (int)(shape[0]*ratio)), interpolation=cv.INTER_LINEAR)
            shape = img.shape
        panH = 200-shape[0]
        panH = (int)(panH/2)
        panW = 200-shape[1]
        panW = (int)(panW/2)

        for h in range(shape[0]):
            for w in range(shape[1]):
                black_img[h+panH][w+panW] = img[h][w]

        black_img = black_img.astype(np.float32)
        black_img = np.multiply(black_img, 1.0 / 255.0)
        self._images.append(black_img)
        self._labels.append(label)
        if expansion == 0:
            return
        # cv.imshow('black', black_img)
        pan = (int)(panW/2)
        left_img = cv.warpAffine(black_img, np.float32(
            [[1, 0, -pan], [0, 1, 0]]), (size, size))

        left_img = left_img.astype(np.float32)
        left_img = np.multiply(left_img, 1.0 / 255.0)
        self._images.append(left_img)
        self._labels.append(label)
        # cv.imshow('left', left_img)

        right_img = cv.warpAffine(black_img, np.float32(
            [[1, 0, pan], [0, 1, 0]]), (size, size))
        right_img = right_img.astype(np.float32)
        right_img = np.multiply(right_img, 1.0 / 255.0)
        self._images.append(right_img)
        self._labels.append(label)
        # cv.imshow('right', right_img)

        pan = (int)(panH/2)
        top_img = cv.warpAffine(black_img, np.float32(
            [[1, 0, 0], [0, 1, -pan]]), (size, size))
        top_img = top_img.astype(np.float32)
        top_img = np.multiply(top_img, 1.0 / 255.0)
        self._images.append(top_img)
        self._labels.append(label)
        # cv.imshow('top', top_img)

        bottom_img = cv.warpAffine(black_img, np.float32(
            [[1, 0, pan], [0, 1, 0]]), (size, size))
        bottom_img = bottom_img.astype(np.float32)
        bottom_img = np.multiply(bottom_img, 1.0 / 255.0)
        self._images.append(bottom_img)
        self._labels.append(label)
        # cv.imshow('bottom', bottom_img)

        # cv.waitKey()

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
                # cv.imshow('img', img)
                for line in lines:
                    line_dict = eval(line)
                    if self._bodyPos != None:
                        if line_dict['status'][0] != self._bodyPos:
                            continue
                    cut_img = cutImage(
                        img, line_dict['left'], line_dict['top'], line_dict['width'], line_dict['height'])

                    label = np.zeros(3)
                    index = self._classess.index(line_dict['status'])
                    if index == 3 or index == 6:
                        index = 0
                    elif index == 4 or index == 7:
                        index = 1
                    elif index == 5 or index == 8:
                        index = 2
                    label[index] = 1.0

                    if line_dict['status'][-5:] != 'study':
                        self.Expansion(cut_img, label)
                    else:
                        self.Expansion(cut_img, label, expansion=0)
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

            if index == 3 or index == 6:
                index = 0
            elif index == 4 or index == 7:
                index = 1
            elif index == 5 or index == 8:
                index = 2

            label = np.zeros(3)
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
        # self._cls = np.array(self._cls)
        # self._images, self._labels, self._cls = shuffle(
        #     self._images, self._labels, self._cls)

        # for i in range(1000):
        #     img = self._images[i]
        #     lab = self._labels[i]
        #     c = self._cls[i]
        #     # img = list(img)
        #     cv.imshow(str(c), img)
        #     cv.waitKey()
    def saveImage(self, filePath):
        count_sleep = 0
        count_telephone = 0
        count_study = 0

        for i in range(len(self._labels)):
            if self._labels[i] == 0:
                cv.imwrite(filePath+'\\sleep\\' +
                           str(count_sleep), self._images[i])
                count_sleep += 1
            elif self._labels[i] == 1:
                cv.imwrite(filePath+"\\telephone\\" +
                           str(count_telephone), self._images[i])
                count_telephone += 1
            else:
                cv.imwrite(filePath+"\\study\\" +
                           str(count_study), self._images[i])
                count_study += 1
        

    def next_batch(self, batchSize):
        end = self._pointer + batchSize
        if end > self._dataSetSize:
            assert batchSize <= self._dataSetSize
            end %= self._dataSetSize
            start = self._pointer
            imgA = self._images[start:]
            imgB = self._images[0:end]
            labelA = self._labels[start:]
            labelB = self._labels[0:end]
            clsA = self._cls[start:]
            clsB = self._cls[0:end]
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

# filePath = ['/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-05/2',
        # '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2018-12-27/1',
        # '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2018-12-27/2',
        # '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2018-12-27/3',
        # '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-17/1',
        # '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-17/2',
        # '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-05/修改间隔后/4',
        # '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-05/修改间隔后/5'
        # ]
# txtPath = ['/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-05/body2',
        #    '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2018-12-27/body1',
        #    '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2018-12-27/body2',
        #    '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2018-12-27/body3',
        #    '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-17/body1',
        #    '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-17/body2',
        #    '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-05/修改间隔后/body4',
        #    '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-05/修改间隔后/body5'
        #    ]
# filePath = ['/Volumes/Seagate Backup Plus Drive/服务外包/picture/tset/1']
# txtPath = ['/Volumes/Seagate Backup Plus Drive/服务外包/picture/tset/body']


# classes = ['right_sleep', 'right_play_telephone', 'right_study',
#            'left_sleep', 'left_play_telephone', 'left_study',
#            'center_sleep', 'center_play_telephone', 'center_study']

# dataSetT = dataSet(filePath, classes, 'txt', txtPath=txtPath)
# dataSetT = dataSet('/Volumes/Seagate Backup Plus Drive/服务外包/picture/2019-03-05/body1', classes, 'image', txtPath=txtPath)
# batchX, batchY, _ = dataSetT.next_batch(64)
# shape = batchX.shape
# print(shape)

# imgs, labels, classess = dataSetT.next_batch(48)

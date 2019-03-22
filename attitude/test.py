import cv2 as cv
import numpy as np
import random

image1 = cv.imread('1.jpg')
image2 = cv.imread('89.jpg')
img = []
img.append(image1)
img.append(image2)

label1 = [0,1]
label2 = [1,0]
label = []
label.append(label1)
label.append(label2)

img = np.array(img)
label = np.array(label)

c = list(zip(img,label))
random.shuffle(c)
img[:],label[:] = zip(*c)
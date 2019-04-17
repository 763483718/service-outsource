import cv2 as cv
import sys
from PIL import Image

from sklearn.utils import shuffle
import requests
import numpy as np
import base64
import glob
import json

def CatchUsbVideo(window_name):
    cv.namedWindow(window_name)

    #告诉OpenCV使用人脸识别分类器
    classfier = cv.CascadeClassifier("/usr/local/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_alt2.xml")
    
    #识别出人脸后要画的边框的颜色，RGB格式
    color = (255, 255, 0)
        
    paths = '/Volumes/Seagate Backup Plus Drive/义乌拍摄/1/**.jpg'
    paths = glob.glob(paths)
    shuffle(paths)
    
    for path in paths:
        img = cv.imread(path)
 
        #将当前帧转换成灰度图像
        grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)                 
        
        #人脸检测，1.2和2分别为图片缩放比例和需要检测的有效点数
        faceRects = classfier.detectMultiScale(grey, scaleFactor = 1.2, minNeighbors = 3, minSize = (32, 32))
        if len(faceRects) > 0:            #大于0则检测到人脸                                   
            for faceRect in faceRects:  #单独框出每一张人脸
                x, y, w, h = faceRect        
                cv.rectangle(img, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 2)
                        
        #显示图像
        shape = img.shape
        img = cv.resize(img,((int)(shape[1]/2),(int)(shape[0]/2)),interpolation=cv.INTER_NEAREST)
        cv.imshow(window_name, img)        
        c = cv.waitKey()
        if c & 0xFF == ord('q'):
            break        
    
    #销毁所有窗口
    cv.destroyAllWindows() 
    
def main():
    CatchUsbVideo("识别人脸区域")
main()

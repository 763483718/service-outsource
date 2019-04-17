from sklearn.utils import shuffle
import requests
import cv2 as cv
import numpy as np
import base64
import glob
import json


def cutImage(img, x, y, w, h):
    return img[y:y+h, x:x+w]


class API():
    def __init__(self):

        self._data = {"api_key": "-em_2KoIyvcsANQ_Lb3lx6XLK1TzYMh8",
                      "api_secret": "Am6aeBkZ4k6xMGLbS9XK7nC07LZvSjPu"}

        self._urls = {'HumanBody_Skeleton': 'https://api-cn.faceplusplus.com/humanbodypp/v1/skeleton',
                      'HumanBody_Detect': 'https://api-cn.faceplusplus.com/humanbodypp/v1/detect',
                      'HumanBody_Segment': 'https://api-cn.faceplusplus.com/humanbodypp/v2/segment',
                      'Face_Detect': 'https://api-cn.faceplusplus.com/facepp/v3/detect',
                      'Face_Compare': 'https://api-cn.faceplusplus.com/facepp/v3/compare'}

    # moudle [in] 功能  more_return [in] 增加请求可选项，2纬数组，分别表示key,value
    def request(self, moudle, image=None, filePath=None, more_return=None):
        if np.all(image == None) and filePath == None:
            return
        if np.all(image == None) == None:
            image = cv.imread(filePath)
        if more_return != None:
            self._data[more_return[0]] = more_return[1]

        buffer = cv.imencode('.jpg', image)
        files = {"image_file": buffer[1]}
        url = self._urls[moudle]

        # 发送post请求
        print('send post\n')
        response = requests.post(url, self._data, files=files)
        print('get response\n')
        req_con = response.content.decode('utf-8')
        print(req_con)

        if moudle == 'Face_Detect':
            return self.Face_Detect(req_con)

    def Face_Detect(self, req_con):
        rects = []
        req_json = json.loads(req_con)
        faces = req_json['faces']
        for face in faces:
            rect = {}
            face_rectangle = face['face_rectangle']
            rect['width'] = face_rectangle['width']
            rect['top'] = face_rectangle['top']
            rect['left'] = face_rectangle['left']
            rect['height'] = face_rectangle['height']
            rects.append(rect)
        return rects


def main():
    paths = '/Volumes/Seagate Backup Plus Drive/义乌拍摄/3/**.jpg'
    paths = glob.glob(paths)
    api = API()
    for path in paths:
        img = cv.imread(path)
        shape = img.shape
        img = cv.resize(img, ((int)(shape[1]/2), (int)
                              (shape[0]/2)), interpolation=cv.INTER_LINEAR)
        rects = api.request('Face_Detect', image=img)
        p1 = path.rfind('/')
        p2 = path.rfind('.')
        num = path[p1+1:p2]
        facepath = './set/study/face/' + num + '.jpg'
        for i in range(len(rects)):
            rect = rects[i]

            cut_img = cutImage(
                img, rect['left'], rect['top'], rect['width'], rect['height'])
            cv.imshow('cut', cut_img)

            imgCopy = np.zeros(shape=img.shape, dtype=np.uint8)
            imgCopy = img.copy()
            cv.rectangle(imgCopy, (rect['left'], rect['top']), (
                rect['left']+rect['width'], rect['top']+rect['height']), [255, 100, 100], 1)

            cv.imshow('face', imgCopy)

            cv.imwrite(facepath, cut_img)
            cv.waitKey()
            del imgCopy


main()

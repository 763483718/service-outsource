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
        if np.all(image == None):
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
        if moudle == 'HumanBody_Skeleton':
            return self.HumanBody_Skeleton(req_con)
        if moudle == 'HumanBody_Segment':
            return self.HumanBody_Segment(req_con)

    def HumanBody_Segment(self, req_con):
        req_json = json.loads(req_con)
        img_b64decode = base64.b64decode(req_json['result'])  # base64解码
        nparr = np.fromstring(img_b64decode, np.uint8)
        img = cv.imdecode(nparr, cv.COLOR_BAYER_BG2RGB)
        cv.imshow('img', img)
        cv.waitKey()

    def HumanBody_Skeleton(self, req_con):
        rects = []
        points = []
        lines = []
        req_json = json.loads(req_con)
        skeletons = {}
        try:
            skeletons = req_json['skeletons']
        except KeyError:
            return rects, points, lines

        for body in skeletons:
            rect = {}
            point = []
            body_rectangle = body['body_rectangle']
            rect['width'] = body_rectangle['width']
            rect['top'] = body_rectangle['top']
            rect['left'] = body_rectangle['left']
            rect['height'] = body_rectangle['height']
            rects.append(rect)
            landmark = body['landmark']

            # 连线数据
            line = []
            line.append([landmark['head'], landmark['neck']])
            line.append([landmark['neck'], landmark['left_shoulder']])
            line.append([landmark['neck'], landmark['right_shoulder']])
            line.append([landmark['left_shoulder'], landmark['left_elbow']])
            line.append([landmark['right_shoulder'], landmark['right_elbow']])
            line.append([landmark['left_elbow'], landmark['left_hand']])
            line.append([landmark['right_elbow'], landmark['right_hand']])
            line.append([landmark['neck'], landmark['left_buttocks']])
            line.append([landmark['neck'], landmark['right_buttocks']])
            lines.append(line)

            for i in landmark:
                if i == 'left_knee' or i == 'right_knee' or i == 'left_foot' or i == 'right_foot' or i == 'left_buttocks' or i == 'right_buttocks':
                    continue
                temp = landmark[i]
                x = temp['x']
                y = temp['y']
                point.append([x, y])
            points.append(point)
        return rects, points, lines


def main():
    # count = 0
    # print(count, '\n\n\n')

    paths = '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2018-12-27/3/**.jpg'
    paths = glob.glob(paths)
    shuffle(paths)
    api = API()

    reStart = 0
    lastNum = 1
    for path in paths:
        p1 = path.rfind('/')
        p2 = path.rfind('.')
        num = path[p1+1:p2]

        if reStart == 0:
            if num == str(lastNum):
                reStart = 1
            else:
                continue

        img = cv.imread(path)
        shape = img.shape
        img = cv.resize(img, ((int)(shape[1]/2), (int)
                              (shape[0]/2)), interpolation=cv.INTER_LINEAR)
        rects, points, lines = api.request('HumanBody_Skeleton', image=img)

        savePath = '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2018-12-27/body3/'
        savePath = savePath + str(num) + '.txt'
        
        if len(rects) == 0:
                continue
        f = open(savePath, 'a')
        for i in range(len(rects)):
            rect = rects[i]

            # count += 1

            cut_img = cutImage(
                img, rect['left'], rect['top'], rect['width'], rect['height'])
            # rect_str = str(rect['left'])+str(rect['top']) + \
            #     str(rect['width'])+str(rect['height'])
            cv.imshow('cut', cut_img)

            imgCopy = np.zeros(shape=img.shape, dtype=np.uint8)
            imgCopy = img.copy()

            point = points[i]
            cv.rectangle(imgCopy, (rect['left'], rect['top']), (
                rect['left']+rect['width'], rect['top']+rect['height']), [255, 100, 100], 1)
            for p in point:
                cv.circle(imgCopy, (p[0]+rect['left'],
                                    p[1]+rect['top']), 2, [100, 255, 100], 1)
            c = 50
            for l in lines[i]:
                cv.line(imgCopy, (l[0]['x']+rect['left'], l[0]['y']+rect['top']),
                        (l[1]['x']+rect['left'], l[1]['y']+rect['top']), [c, c, 200])
                c += 30

            cv.imshow(num, imgCopy)

            test = cv.waitKey()

            if test == ord('a'):
                # CApath = savePath + 'center/sleep/' + str(count) + '.jpg'
                # cv.imwrite(CApath, cut_img)
                rect['status'] = 'center_sleep'
                del imgCopy

            elif test == ord('s'):
                # CBpath = savePath + 'center/play telephone/' + str(count) + '.jpg'
                # cv.imwrite(CBpath, cut_img)
                rect['status'] = 'center_play_telephone'
                del imgCopy

            elif test == ord('d'):
                # CCpath = savePath + 'center/study/' + str(count) + '.jpg'
                # cv.imwrite(CCpath, cut_img)
                rect['status'] = 'center_study'
                del imgCopy

            elif test == ord('q'):
                # LApath = savePath + 'left/sleep/' + str(count) + '.jpg'
                # cv.imwrite(LApath, cut_img)
                rect['status'] = 'left_sleep'
                del imgCopy

            elif test == ord('w'):
                # LBpath = savePath + 'left/play telephone/' + str(count) + '.jpg'
                # cv.imwrite(LBpath, cut_img)
                rect['status'] = 'left_play_telephone'
                del imgCopy

            elif test == ord('e'):
                # LCpath = savePath + 'left/study/' + str(count) + '.jpg'
                # cv.imwrite(LCpath, cut_img)
                rect['status'] = 'left_study'
                del imgCopy

            elif test == ord('z'):
                # RApath = savePath + 'right/sleep/' + str(count) + '.jpg'
                # cv.imwrite(RApath, cut_img)
                rect['status'] = 'right_sleep'
                del imgCopy

            elif test == ord('x'):
                # RBpath = savePath + 'right/play telephone/' + str(count) + '.jpg'
                # cv.imwrite(RBpath, cut_img)
                rect['status'] = 'right_play_telephone'
                del imgCopy

            elif test == ord('c'):
                # RCpath = savePath + 'right/study/' + str(count) + '.jpg'
                # cv.imwrite(RCpath, cut_img)
                rect['status'] = 'right_study'
                del imgCopy

            else:
                continue
            
            f.write(str(rect))
            f.write('\n')
        f.close()

        cv.destroyWindow(num)


main()

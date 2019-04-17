import cv2
 
def video_picture(videoPath, savePath, f):
    
    #获得视频的格式
    videoCapture = cv2.VideoCapture(videoPath)
    
    #获得码率及尺寸
    # fps = videoCapture.get(cv2.cv.CV_CAP_PROP_FPS)
    
    #读帧
    success, frame = videoCapture.read()

    count = 0
    num = 1
    while success :
        # cv2.imshow("cut_picture", frame) #显示
        #cv2.waitKey(1000/int(fps)) #延迟
        count += 1
        if count % f == 1:
            path = savePath + str(num) + '.jpg'
            # 获取图片尺寸并计算图片中心点
            #(h, w) = frame.shape[:2]
            #center = (w/2, h/2)

            # 将图像旋转180度
            #M = cv2.getRotationMatrix2D(center, 180, 1.0)
            #rotated = cv2.warpAffine(frame, M, (w, h))
            #cv2.imwrite(path, rotated)

            cv2.imwrite(path, frame)
            num += 1
            #del rotated
        del frame
        
        success, frame = videoCapture.read() #获取下一帧

def main():
    videoPath = '/Volumes/Seagate Backup Plus Drive/服务外包/视频/2018-12-27/1.mp4'
    savePath = '/Volumes/Seagate Backup Plus Drive/服务外包/picture/2018-12-27/1/'
    # videoPath = '/Volumes/Seagate Backup Plus Drive/义乌拍摄/3.MP4'
    # savePath = '/Volumes/Seagate Backup Plus Drive/义乌拍摄/3/'
    video_picture(videoPath, savePath, 200)

main()
import cv2


def video2frames(videoname):
    print(cv2.__version__)
    vidcap = cv2.VideoCapture(videoname)
    success, image = vidcap.read()
    count = 0
    while success:
        # save frame as BMP file
        cv2.imwrite("data/frame%d.bmp" % count, image)
        success, image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1

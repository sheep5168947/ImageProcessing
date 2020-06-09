import cv2


def video2frames(videoname, num):
    print(cv2.__version__)
    vidcap = cv2.VideoCapture(videoname)
    success, image = vidcap.read()
    count = 0
    path = ['data', 'ghost']
    while success:
        # save frame as BMP file
        if num == 0:
            cv2.imwrite(path[0]+"/frame%d.png" % count, image)
        else:
            cv2.imwrite(path[1]+"/frame%d.png" % count, image)
        success, image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1

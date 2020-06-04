import random
import functionality
import video2frames
import frames2video


# ------------------------------
#影片轉成圖片
videoname = 'drop3.avi'
video2frames.video2frames(videoname)


# ------------------------------
# 這裡把圖片放上小人
#還有實作那些功能





# -------------------------------
#圖片轉回影片
inputpath = 'data'
outputname =  'newvideo.avi'
fps = 29
frames2video.frames_to_video(inputpath,outputname,fps)


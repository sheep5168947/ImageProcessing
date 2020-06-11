import random
import functionality
import video2frames
import frames2video


# ------------------------------
#宣告用
videoname1 = 'drop3.avi'
inputpath = ['data','ghost']
combineimg = "combine_img"
outputname =  'newvideo.avi'
fps = 29

# ------------------------------
#影片轉成圖片
# video2frames.video2frames(videoname1,0)

# ------------------------------
# 這裡把圖片放上小人
functionality.combine(inputpath[0],inputpath[1])


#還有實作那些功能









# -------------------------------
#圖片轉回影片

frames2video.frames_to_video(combineimg,outputname,fps)


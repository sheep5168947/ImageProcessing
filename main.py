import random
import functionality
import video2frames
import frames2video
import SpecialEffects

# ------------------------------
#宣告用
videoname1 = 'ohoh.mp4'
inputpath = ['data','ghost','left-ghost','right-ghost','up-ghost']
combineimg = "combine_img"
outputname =  'newvideo.avi'
fps = 29

# ------------------------------
#影片轉成圖片
video2frames.video2frames(videoname1,0)

# ------------------------------
# 這裡把圖片放上小人
functionality.combine(inputpath)


#還有實作那些功能









# -------------------------------
#圖片轉回影片

frames2video.frames_to_video(combineimg,outputname,fps)


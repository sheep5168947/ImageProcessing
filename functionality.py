import numpy as np
import os
from PIL import Image
import SpecialEffects
import random
import copy
import cv2
from cv2 import cv2 as cv2
import Effect
# -------------------------------------
# 全域變數
cross = 20
gj = 0
gl = 0
gr = 0
gu = 0
gx = 0
gy = 360
flag = 0
count = 0
rem = 0
# --------------------------------------
# 定義那些放大啥小的功能


def ghostjump(inputpath):
    global gj
    ghostjump = [f for f in os.listdir(inputpath[1]) if os.path.isfile(
        os.path.join(inputpath[1], f))]
    ghostjump.sort(key=lambda x: int(x[5:-4]))

    ghostjumpImg = Image.open(inputpath[1] + '/' + ghostjump[gj])  # 鬼跑跳

    if gj == len(ghostjump)-1:
        gj = 0
    else:
        gj += 1

    return ghostjumpImg


def ghostleft(inputpath):

    global gl
    ghostleft = [f for f in os.listdir(inputpath[2]) if os.path.isfile(
        os.path.join(inputpath[2], f))]
    ghostleft.sort(key=lambda x: int(x[5:-4]))

    ghostleftImg = Image.open(inputpath[2] + '/' + ghostleft[gl])  # 鬼跑跳

    if gl == len(ghostleft)-1:
        gl = 0
    else:
        gl += 1
    return ghostleftImg


def ghostright(inputpath):
    global gr
    ghostright = [f for f in os.listdir(inputpath[3]) if os.path.isfile(
        os.path.join(inputpath[3], f))]
    ghostright.sort(key=lambda x: int(x[5:-4]))

    ghostrightImg = Image.open(inputpath[3] + '/' + ghostright[gr])  # 鬼跑跳

    if gr == len(ghostright)-1:
        gr = 0
    else:
        gr += 1

    return ghostrightImg


def ghostup(inputpath):
    global gu
    ghostup = [f for f in os.listdir(inputpath[4]) if os.path.isfile(
        os.path.join(inputpath[4], f))]
    ghostup.sort(key=lambda x: int(x[5:-4]))

    ghostupImg = Image.open(inputpath[4] + '/' + ghostup[gu])  # 鬼跑跳

    if gu == len(ghostup)-1:
        gu = 0
    else:
        gu += 1

    return ghostupImg


facePos = [-1, -1, -1, -1]


def combine(inputpath):
    global gx, gy, flag, facePos,count,rem
    textx = 0
    texty = 0
    x = 0
    y = 0
    # 讀檔 ------------------------------------

    basemap = [f for f in os.listdir(inputpath[0]) if os.path.isfile(
        os.path.join(inputpath[0], f))]
    basemap.sort(key=lambda x: int(x[5:-4]))

    # ------------------------------------------

    for i in range(len(basemap)):
        if i % 30 == 0:
            print('以處理', i)
        # 讀每一張圖-------------------------------
        basemapImg = Image.open(inputpath[0] + '/' + basemap[i])  # 底圖
        basemapImg = basemapImg.convert('RGBA')
        basemapW, basemapH = basemapImg.size

        BI = cv2.imread(inputpath[0] + '/' + basemap[i])
        # 實做特效--------------------------------
        # 偵測臉部位置
        faceList = SpecialEffects.FaceDection(BI)
        # print(faceList)
        if len(faceList) > 0:
            if facePos[0] == -1:
                # 表示目前沒有正在追蹤的臉
                faceNum = random.randint(0, len(faceList)-1)
                for j in range(4):
                    facePos[j] = faceList[faceNum][j]
            else:
                # 目前有跟蹤的臉
                # 找到與上一張臉最相近的臉yaaa
                faceNum = 0  # 這裡是不是會一直蓋到
                minDic = (faceList[0][0]-facePos[0])**2 + \
                    (faceList[0][1]-facePos[1])**2
                for j in range(len(faceList)):
                    dic = (faceList[j][0]-facePos[0])**2 + \
                        (faceList[j][1]-facePos[1])**2
                    if dic < minDic:
                        minDic = dic
                        faceNum = j
                if faceNum != -1:
                    for L in range(4):
                        facePos[L] = faceList[faceNum][L]
            x = facePos[0]
            y = facePos[1]
        # print(i,x,y)
        textx = int(facePos[2]/2)
        texty = int(facePos[3]/2)
        # 擷取臉部

        # 小人跑到特效那邊，並疊圖存在combine-img裡-------------------------
        deltaX = abs(gx-x)
        deltaY = abs(gy-y)
        if deltaX > 15 or deltaY > 15:
            if gx-x > 15:
                gx -= 5
                if gx - x < 15:
                    gx = x
                    pass
            elif gx-x < 15:
                gx += 5
                if gx-x > 15:
                    gx = x
                    pass
            else:
                pass
            if gy-y > 15:
                gy -= 5
                if gy - y < 15:
                    gy = y
                    pass
            elif gy-y < 15:
                gy += 5
                if gy - y > 15:
                    gy = y
                    pass
            else:
                pass
            ghostjumpW, ghostjumpH = ghostjump(inputpath).size
            newwidth = int(basemapW/3)
            newheight = int(ghostjumpH/ghostjumpW*newwidth)
            newghostjump = ghostjump(inputpath).resize((newwidth, newheight))
            combine_img = Image.new('RGBA', basemapImg.size, (0, 0, 0, 0))
            combine_img.paste(basemapImg, (0, 0))
            textx -= int(0.54*newheight)
            texty -= int(0.286*newwidth)
            combine_img.paste(
                newghostjump, (gx+textx, gy+texty), mask=newghostjump)
            route = "combine_img/frame"+str(i)+".png"
            combine_img.save(route)
            flag = 0
        else:

            # 這裡寫特效+疊圖--------------

            ghostupW, ghostupH = ghostup(inputpath).size
            newwidth = int(basemapW/3)
            newheight = int(ghostupH/ghostupW*newwidth)
            newghostup = ghostup(
                inputpath).resize((newwidth, newheight))

            # 隨機選一個特效----------------------------
            
            if count == 0 :
                chooseEffect = random.randint(0, 3)
            elif count == 120:
                count = 0
            else:
                count+=1
            # 將進行圓形切割
            split = cv2.imread(
                inputpath[0] + '/' + basemap[i], cv2.IMREAD_UNCHANGED)

            splitPos = [facePos[0]-int(newwidth/4-facePos[2]/2), facePos[1]-int(
                newheight/4-facePos[3]/2), int(newheight/2), int(newheight/2)]
            splitImg = SpecialEffects.SplitPicture(
                split, splitPos, "square")

            
            if chooseEffect == 0:
                splitImg = Effect.Negtive(splitImg)
                # 負片
                pass
            elif chooseEffect == 1:
                splitImg = SpecialEffects.BlurFun(splitImg)
                # 模糊
                pass
            elif chooseEffect == 2:
                # 馬賽克
                splitImg = SpecialEffects.MosaicFun(splitImg)
                pass
            elif chooseEffect == 3:
                splitImg = SpecialEffects.hierarchyColor(splitImg, 60)
                # 色階
                pass
            # elif chooseEffect == 4:
            #     splitImg = Effect.Zoom(splitImg,1.2)
            #     # 放大
            #     pass

            splitPos[2] = int(splitPos[2]/2)
            splitImg = SpecialEffects.SplitPicture(
                splitImg, splitPos, "circle")
            cv2.imwrite("split/"+basemap[i], splitImg)  # test

            cover = SpecialEffects.cover(split, splitImg, [0, 0])
            cv2.imwrite(inputpath[0] + '/' + basemap[i], cover)

            basemapImg = Image.open(inputpath[0] + '/' + basemap[i])  # 底圖
            basemapImg = basemapImg.convert('RGBA')
            basemapW, basemapH = basemapImg.size
           # 進行特效處理

            # ---------------------------

            textx -= int(0.54*newheight)
            texty -= int(0.286*newwidth)

            combine_img = Image.new(
                'RGBA', basemapImg.size, (0, 0, 0, 0))
            combine_img.paste(basemapImg, (0, 0))
            combine_img.paste(newghostup,  (gx+textx, gy+texty),
                              mask=newghostup)
            route = "combine_img/frame"+str(i)+".png"
            combine_img.save(route)

    return

import numpy as np
import os
from PIL import Image
import SpecialEffects
import random
import copy
import cv2 as cv
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


def combine(inputpath):
    global gx, gy, flag
    textx = 0
    texty = 0
    x = 0
    y = 0
    # 讀檔 ------------------------------------

    basemap = [f for f in os.listdir(inputpath[0]) if os.path.isfile(
        os.path.join(inputpath[0], f))]
    basemap.sort(key=lambda x: int(x[5:-4]))

    # ------------------------------------------


    facePos = [-1, -1, -1, -1]
    # 隨機選一個特效----------------------------
    chooseEffect = random.randint(0, 4)
    for i in range(len(basemap)):
        if i % 30 == 0:
            print('以處理', i)
        # 讀每一張圖-------------------------------
        basemapImg = Image.open(inputpath[0] + '/' + basemap[i])  # 底圖
        basemapImg = basemapImg.convert('RGBA')
        basemapW, basemapH = basemapImg.size

        BI = cv.imread(inputpath[0] + '/' + basemap[i])
        # 實做特效--------------------------------
        # 偵測臉部位置
        faceList = SpecialEffects.FaceDection(BI)
        if facePos[0] == -1 and len(faceList) > 0:
            # 表示目前沒有正在追蹤的臉
            faceNum = random.randint(0, len(faceList)-1)
            for j in range(4):
                facePos[j] = faceList[faceNum][j]
        else:
            # 找到與上一張臉最相近的臉
            faceNum = -1
            minDic = 0
            for j in range(len(faceList)):
                dic = (faceList[j][0]-facePos[0])**2 + \
                    (faceList[j][1]-facePos[1])**2
                if dic < minDic:
                    minDic = dic
                    faceNum = j
            if faceNum != -1:
                facePos = copy.deepcopy(faceList[faceNum])
            x = facePos[0]
            y = facePos[1]
            textx = int(facePos[2]/2)
            texty = int(facePos[3]/2)
        # 擷取臉部

        # 進行特效處理
        # if chooseEffect == 0:
        #     # 放大
        # elif chooseEffect == 1:
        #     asd
        # elif chooseEffect == 2:

        # elif chooseEffect == 3:

        # elif chooseEffect == 4:
            # 將特效後的臉進行圓形切割

            # 小人跑到特效那邊，並疊圖存在combine-img裡-------------------------
        if gx != x and gy != y:
            if gx-x > 0:
                gx -= 2
                if gx - x < 0:
                    gx = x
            elif gx-x < 0:
                gx += 2
                if gx-x > 0:
                    gx = x
            else:
                pass
            if gy-y > 0:
                gy -= 2
                if gy - y < 0:
                    gy = y
            elif gy-y < 0:
                gy += 2
                if gy - y > 0:
                    gy = y
            else:
                pass
            ghostjumpW, ghostjumpH = ghostjump(inputpath).size
            newwidth = int(basemapW/4)
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
            raisehand = random.randint(0, 1)
            if flag == 0:
                if raisehand == 0:
                    ghostleftW, ghostleftH = ghostleft(inputpath).size
                    newwidth = int(basemapW/4)
                    newheight = int(ghostleftH/ghostleftW*newwidth)
                    newghostleft = ghostleft(inputpath).resize(
                        (newwidth, newheight))
                    combine_img = Image.new(
                        'RGBA', basemapImg.size, (0, 0, 0, 0))
                    combine_img.paste(basemapImg, (0, 0))
                    textx -= int(0.54*newheight)
                    texty -= int(0.286*newwidth)
                    combine_img.paste(newghostleft, (gx+textx, gy+texty),
                                      mask=newghostleft)
                    route = "combine_img/frame"+str(i)+".png"
                    combine_img.save(route)
                    flag = 1
                else:
                    ghostrightW, ghostrightH = ghostright(inputpath).size
                    newwidth = int(basemapW/4)
                    newheight = int(ghostrightH/ghostrightW*newwidth)
                    newghostright = ghostright(
                        inputpath).resize((newwidth, newheight))
                    combine_img = Image.new(
                        'RGBA', basemapImg.size, (0, 0, 0, 0))
                    combine_img.paste(basemapImg, (0, 0))
                    textx -= int(0.54*newheight)
                    texty -= int(0.286*newwidth)
                    combine_img.paste(newghostright,  (gx+textx, gy+texty),
                                      mask=newghostright)
                    route = "combine_img/frame"+str(i)+".png"
                    combine_img.save(route)
                    flag = 1
            elif flag == 1:
                ghostupW, ghostupH = ghostup(inputpath).size
                newwidth = int(basemapW/4)
                newheight = int(ghostupH/ghostupW*newwidth)
                newghostup = ghostup(
                    inputpath).resize((newwidth, newheight))
                combine_img = Image.new(
                    'RGBA', basemapImg.size, (0, 0, 0, 0))
                combine_img.paste(basemapImg, (0, 0))
                textx -= int(0.54*newheight)
                texty -= int(0.286*newwidth)
                combine_img.paste(newghostup,  (gx+textx, gy+texty),
                                  mask=newghostup)
                route = "combine_img/frame"+str(i)+".png"
                combine_img.save(route)

    return

#coding:utf-8
import cv2
import numpy as np
import time

def SplitPicture(imageData,Pos,shape="square"):
    #分割圖片
    #切正方形
    if shape=="square":
        x=Pos[0]
        y=Pos[1]
        w=Pos[2]
        h=Pos[3]
        #print(x,y,w,h)
        temp= np.array([[[0]*4]*w]*h, dtype=np.uint8)
        #print(len(temp),len(temp[0]))
        for j in range(h):
            for i in range(w):
                temp[j][i][0]=imageData[y+j][x+i][0]
                temp[j][i][1]=imageData[y+j][x+i][1]
                temp[j][i][2]=imageData[y+j][x+i][2]
        #print(len(temp),len(temp[0]))
        return temp
    #切圓形
    if shape=="cycle":
        x=Pos[0]#圓心
        y=Pos[1]#圓心
        r=Pos[2]#半徑
        r_Q=r**2
        temp= np.array([[[0]*4]*r*2]*r*2, dtype=np.uint8)
        #print(len(temp),len(temp[0]))
        #對temp賦予值
        for j in range(r*2):
            for i in range(r*2):
                
                dis=(j-r)**2+(i-r)**2
                if dis>r_Q:
                    temp[j][i][3]=0
                    continue  
                
                temp[j][i][0]=imageData[y-r+j][x-r+i][0]
                temp[j][i][1]=imageData[y-r+j][x-r+i][1]
                temp[j][i][2]=imageData[y-r+j][x-r+i][2]
        #print(len(temp),len(temp[0]))
        return temp

def Negtive(imageData) :
    #負片
    w = imageData.shape[1] #原圖的寬
    h = imageData.shape[0] #原圖的高
 
    #產生一個空的圖
    new_img = np.zeros((h, w, 3), dtype=np.uint8)

    #作負片
    for xi in range(0,w) :
        for yi in range(0,h) :
            new_img[yi,xi,0] = 255 - imageData[yi,xi,0]
            new_img[yi,xi,1] = 255 - imageData[yi,xi,1]
            new_img[yi,xi,2] = 255 - imageData[yi,xi,2]
    
    return new_img

def Zoom(imageData, ratio) :
    #放大圖片
    ori_h, ori_w = imageData.shape[:2] # 原圖的寬高
    new_h = int(imageData.shape[0] * ratio) #新圖的高
    w_ratio = new_h/ori_h #計算寬度放大比例
    new_w = int(imageData.shape[1] * w_ratio) #新圖的寬
    
    scale_x = float(ori_w) / new_w # X的缩放比例
    scale_y = float(ori_h) / new_h # Y的缩放比例
    #print(scale_x, scale_y)

    #產生一個空的圖
    temp = np.zeros((new_h, new_w, 3), dtype=np.uint8)
    #作插值
    for n in range(3): #RGB的LOOP
        for new_y in range(new_h): #對高的LOOP
            for new_x in range(new_w):  #對寬的LOOP
                ori_x = (new_x + 0.5) * scale_x - 0.5
                ori_y = (new_y + 0.5) * scale_y - 0.5
                # 計算四個鄰近點的值
                ori_x_0 = int(np.floor(ori_x))
                ori_y_0 = int(np.floor(ori_y))
                ori_x_1 = min(ori_x_0 + 1, ori_w - 1)
                ori_y_1 = min(ori_y_0 + 1, ori_h - 1)

                # 雙線性內插
                value0 = (ori_x_1 - ori_x) * imageData[ori_y_0, ori_x_0, n] + (ori_x - ori_x_0) * imageData[ori_y_0, ori_x_1, n]
                value1 = (ori_x_1 - ori_x) * imageData[ori_y_1, ori_x_0, n] + (ori_x - ori_x_0) * imageData[ori_y_1, ori_x_1, n]
                temp[new_y, new_x, n] = int((ori_y_1 - ori_y) * value0 + (ori_y - ori_y_0) * value1)
    #產生一個空的圖與原圖大小相同
    # new_img = np.zeros((ori_h, ori_w, 3), dtype=np.uint8)
    # x = int(new_w/2)
    # y = int(new_h/2)
    # #切下放大後的圖
    # new_img = SplitPicture(temp,(x,y,r),shape= 'cycle')
    return temp
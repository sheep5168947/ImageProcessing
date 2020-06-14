import os
import cv2 as cv
import numpy as np
import time
import copy
def BlurFun(imageData,maskSize=5):
    # 模糊效果
    #image= cv.imread("data\\frame0.bmp")
    image= imageData
    #temp= np.array([[[0]*3]*len(image[0])]*len(image), dtype=np.int16)
    temp= np.array(imageData, dtype=np.int16)
    new_image= copy.deepcopy(image)
    mask_size=maskSize
    mask_size_2=int(mask_size/2)
    mask_size_Q=mask_size**2
    tStart = time.time()
    for i in range(mask_size_2,len(image)-mask_size_2):
        for j in range(mask_size_2,len(image[0])-mask_size_2):
            sumR=image[i][j][0]
            sumG=image[i][j][1]
            sumB=image[i][j][2]
            for ai in range(-mask_size_2,mask_size_2+1):
                for aj in range(-mask_size_2,mask_size_2+1):
                    temp[i+ai][j+aj][0]+=sumR
                    temp[i+ai][j+aj][1]+=sumG
                    temp[i+ai][j+aj][2]+=sumB

    for i in range(0,len(image)):
        for j in range(0,len(image[0])):
            new_image[i][j][0]=(temp[i][j][0]/mask_size_Q).astype('uint8')
            new_image[i][j][1]=(temp[i][j][1]/mask_size_Q).astype('uint8')
            new_image[i][j][2]=(temp[i][j][2]/mask_size_Q).astype('uint8')
            
            if i<=mask_size_2 or i>=len(image)-mask_size_2-1:
                new_image[i][j][0]=image[i][j][0]
                new_image[i][j][1]=image[i][j][1]
                new_image[i][j][2]=image[i][j][2]
            if j<=mask_size_2 or j>=len(image[0])-mask_size_2-1:
                new_image[i][j][0]=image[i][j][0]
                new_image[i][j][1]=image[i][j][1]
                new_image[i][j][2]=image[i][j][2]
            
    tEnd = time.time()
    #print ("B cost %f sec" % (tEnd - tStart))
    #cv.imshow('new_image5',new_image)
    return new_image


def MosaicFun(imageData,maskSize=10):
    #馬賽克效果
    image= imageData
    new_image= imageData 
    mosaic_size=maskSize 
    mosaic_size_Q=mosaic_size*mosaic_size 
    maxHeight=0
    maxWight=0
    tStart = time.time()
    for i in range(0,len(image)-mosaic_size,mosaic_size):
        maxHeight=i
        for j in range(0,len(image[0])-mosaic_size,mosaic_size):
            #print("i %d j %d",i,j)
            maxWight=j
            SumR=0
            SumG=0
            SumB=0
            for ai in range(mosaic_size):
                for aj in range(mosaic_size):
                    SumR+=image[i+ai][j+aj][0].astype("int16")
                    SumG+=image[i+ai][j+aj][1].astype("int16")
                    SumB+=image[i+ai][j+aj][2].astype("int16")
            SumR=(SumR/mosaic_size_Q).astype('uint8')
            SumG=(SumG/mosaic_size_Q).astype('uint8')
            SumB=(SumB/mosaic_size_Q).astype('uint8')

            for ai in range(mosaic_size):
                for aj in range(mosaic_size):
                    new_image[i+ai][j+aj][0]=SumR
                    new_image[i+ai][j+aj][1]=SumG
                    new_image[i+ai][j+aj][2]=SumB
    #修正下排
    for j in range(0,len(image[0])-mosaic_size,mosaic_size):
        SumR=0
        SumG=0
        SumB=0  
        size= (len(image)-maxHeight)* mosaic_size    
        for ai in range(maxHeight,len(image)):
            for aj in range(mosaic_size):  
                    SumR+=image[ai][j+aj][0].astype("int16")
                    SumG+=image[ai][j+aj][1].astype("int16")
                    SumB+=image[ai][j+aj][2].astype("int16")
        SumR=(SumR/size).astype('uint8')
        SumG=(SumG/size).astype('uint8')
        SumB=(SumB/size).astype('uint8')         
        for ai in range(maxHeight,len(image)):
            for aj in range(mosaic_size):
                new_image[ai][j+aj][0]=SumR
                new_image[ai][j+aj][1]=SumG
                new_image[ai][j+aj][2]=SumB    
    #修正右排
    for i in range(0,len(image)-mosaic_size,mosaic_size):
        SumR=0
        SumG=0
        SumB=0  
        size= (len(image[0])-maxWight)* mosaic_size    
        for ai in range(mosaic_size):
            for aj in range(maxWight,len(image[0])):  
                    SumR+=image[ai+i][aj][0].astype("int16")
                    SumG+=image[ai+i][aj][1].astype("int16")
                    SumB+=image[ai+i][aj][2].astype("int16")
        SumR=(SumR/size).astype('uint8')
        SumG=(SumG/size).astype('uint8')
        SumB=(SumB/size).astype('uint8')
        for ai in range(mosaic_size):
            for aj in range(maxWight,len(image[0])):  
                new_image[ai+i][aj][0]=SumR
                new_image[ai+i][aj][1]=SumG
                new_image[ai+i][aj][2]=SumB  
    tEnd = time.time()
    print(len(image),len(image[0]))
    print("H,W=",maxHeight,maxWight)
    #print ("B cost %f sec" % (tEnd - tStart))
    return new_image

def hierarchyColor(imageData,level):
    level_2=int(level/2)
    for i in range (len(imageData)):
        for j in range(len(imageData[0])):
            imageData[i][j][0]=(int((imageData[i][j][0]+level_2)/level)*level)
            imageData[i][j][1]=(int((imageData[i][j][1]+level_2)/level)*level)
            imageData[i][j][2]=(int((imageData[i][j][2]+level_2)/level)*level)
    return imageData


def FaceDection(imageData):
    #臉部偵測
    face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
    face_cascade.load("C:\\Users\\pan\\Desktop\\ImageProcessing\\haarcascade_frontalface_default.xml")
    # 讀取圖片
    img = imageData
    # 轉成灰階圖片
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # 偵測臉部
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.08,
        minNeighbors=5,
        minSize=(32, 32))

    return faces

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

def cover(orginImage,covered,Pos):
    #將原圖片覆蓋上其他圖片
    channalNum=len(covered[0][0])
    
    x=Pos[0]
    y=Pos[1]
    for i in range(len(covered)):
        for j in range(len(covered[0])):
            if y+j>=len(orginImage) or x+i>=len(orginImage[0]):
                continue
            if channalNum==4 and covered[j][i][3]==0:
                continue
            orginImage[y+j][x+i][0]=covered[j][i][0]
            orginImage[y+j][x+i][1]=covered[j][i][1]
            orginImage[y+j][x+i][2]=covered[j][i][2]
    return orginImage
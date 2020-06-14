import numpy as np
import os
from PIL import Image
import SpecialEffects
# -------------------------------------
# 全域變數
cross = 20

#--------------------------------------
# 定義那些放大啥小的功能


def chofun(chosen):
    print(chosen)


def combine(inputpath1, inputpath2):
    files1 = [f for f in os.listdir(inputpath1) if os.path.isfile(
        os.path.join(inputpath1, f))]
    files1.sort(key=lambda x: int(x[5:-4]))
    files2 = [f for f in os.listdir(inputpath2) if os.path.isfile(
        os.path.join(inputpath2, f))]
    files2.sort(key=lambda x: int(x[5:-4]))
    count = 0
    j = 0
    effect = 0
    x = 0
    jump = 0
    convert = 0
    for i in range(len(files1)):

        img1 = Image.open(inputpath1 + '/' + files1[i])
        img1 = img1.convert('RGBA')
        width1, height1 = img1.size

        img2 = Image.open(inputpath2 + '/' + files2[j])
        # img2 = img2.convert('RGBA')
        width2, height2 = img2.size

        newwidth2 = int(width1/2)
        newheight2 = int(height2/width2*newwidth2)

        newimg2 = img2.resize((newwidth2, newheight2))

        combine_img = Image.new('RGBA', img1.size, (0, 0, 0, 0))
        # combine
        combine_img.paste(img1, (0, 0))
        combine_img.paste(newimg2, (x, newheight2), mask=newimg2)
        # combine_img.show()
        route = "combine_img/frame"+str(count)+".png"
        combine_img.save(route)
        if j == len(files2)-1:
            if effect == 20:
                j = 0
                effect = 0
            else:
                effect+=1
            
        elif j == 8:
            if jump == 3:
                jump = 0
                j +=1
            else:
                if convert == 0:
                    x+=cross
                    if x >= newwidth2:
                        convert = 1
                        x-=cross
                elif convert == 1:
                    x-=cross
                    if x <= 0:
                        convert = 0
                        x+=cross
                j = 0
                jump+=1
        elif j == 9 or j == 11:
            if effect == 20:
                j+=1
                effect = 0
            else:
                effect+=1
        else:
            j = j + 1
        count += 1
    return


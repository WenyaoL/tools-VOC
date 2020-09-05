import math
import os
import random
import time
import matplotlib.pyplot as plt
import cv2
import numpy as np
from skimage.util import random_noise


class ImgParser:
    def __init__(self, imgpath=None):
        self.imgpath= imgpath
        if self.imgpath != None:
            self.ImgName = os.path.split(self.imgpath)[-1]
            self.img = cv2.imread(imgpath)

    def setImg(self, path):
        '''
            设置图片，获取图片并用cv2读取图片
        :param path: 图片所在路径
        :return:
        '''
        self.imgpath = path
        self.ImgName = os.path.split(self.imgpath)[-1]
        self.img = cv2.imread(self.imgpath)



    def addNoise_Img(self, img=None):
        '''
            没指定img默认使用class中的图片
        :param img: 新图片
        :return: 加噪声后的图像array
        '''
        if img == None:
            return random_noise(self.img, mode='gaussian', seed=int(time.time())) *255

        return random_noise(img, mode='gaussian', seed=int(time.time())) *255

    def filp_img(self, img=None, filp=1):
        '''

            提供图片翻转,默认反转方式是水平翻转
        :param img: 图像array
        :param filp: 翻转后的图像array
        :return:
        '''
        if img is None:
            img = self.img

        img = cv2.flip(img, filp)  # _flip_
        return img


    def randomfilp_Img(self, img = None):
        '''
                提供图片随机翻转

        :param img: 图像array
        :return: 翻转后的图像array
        '''

        if img is None:
            img =self.img
        # --------------------  翻转图像  ----------------------
        h, w, _ = img.shape
        sed = random.random()
        if 0 < sed < 0.33:
            img = cv2.flip(img, 0)
        elif 0.33 < sed < 0.66:
            img = cv2.flip(img, 1)
        else:
            img = cv2.flip(img, -1)
        return img

    def changeLight_Img(self, img=None,r=None):
        if img is None:
            img =self.img
        if r is None:
            r = random.uniform(0.35, 1)
        blank = np.zeros(img.shape, img.dtype)
        return cv2.addWeighted(img, r, blank, 1 - r, 0)

    def rotate_Img(self, img=None, angle=5, scale=1.):
        '''
        参考:https://blog.csdn.net/u014540717/article/details/53301195
        输入:
            img:图像array,(h,w,c)
            angle:旋转角度
            scale:默认1
        输出:
            rot_img:旋转后的图像array
        '''
        if img is None:
            img = self.img
        # ---------------------- 旋转图像 ----------------------
        w = img.shape[1]
        h = img.shape[0]
        # 角度变弧度
        rangle = np.deg2rad(angle)  # angle in radians
        # now calculate new image width and height
        nw = (abs(np.sin(rangle) * h) + abs(np.cos(rangle) * w)) * scale
        nh = (abs(np.cos(rangle) * h) + abs(np.sin(rangle) * w)) * scale
        # ask OpenCV for the rotation matrix
        rot_mat = cv2.getRotationMatrix2D((nw * 0.5, nh * 0.5), angle, scale)
        # calculate the move from the old center to the new center combined
        # with the rotation
        rot_move = np.dot(rot_mat, np.array([(nw - w) * 0.5, (nh - h) * 0.5, 0]))
        # the move only affects the translation, so update the translation
        rot_mat[0, 2] += rot_move[0]
        rot_mat[1, 2] += rot_move[1]
        # 仿射变换
        rot_img = cv2.warpAffine(img, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))), flags=cv2.INTER_LANCZOS4)
        return rot_img, rot_mat

    def shift_Img(self,x,y,img=None):
        '''
            随机平移图像[-x,x],[-y,y]，默认平移当前图片，
            也可以通过img指定新的图片

        :param x: 平移x范围下[-x,x]
        :param y: 平移y范围[-y,y]
        :param img: 指定新的平移图像
        :return:
        '''

        if img is None:
            img =self.img

        # ---------------------- 平移图像 ----------------------
        x = random.uniform(-x, x)
        y = random.uniform(-y, y)

        M = np.float32([[1, 0, x], [0, 1, y]])  # x为向左或右移动的像素值,正为向右负为向左; y为向上或者向下移动的像素值,正为向下负为向上
        shift_img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))

        return shift_img



if __name__ == '__main__':
    #I =ImgParser(r'.\TestDate\Images\0001.jpg')
    I = ImgParser()
    I.setImg(r'.\TestDate\Images\000004.jpg')
    img5, _ =I.rotate_Img()
    img = [I.addNoise_Img()/255,I.changeLight_Img(),I.filp_img(),I.shift_Img(50,50),img5]

    pic = ['noise', 'changeLight', 'filp', 'shift','rotate']
    plt.figure(figsize=(8,6))
    for i in range(5):
        plt.subplot(2, 3, i + 1)
        plt.imshow(img[i])
        plt.title(pic[i])
    plt.show()
    # 因为要[0,1]的浮点数或[0,255]的整数，由于这里是浮点数，所有要映射回去[0,1]
   # cv2.imshow('img', I.addNoise_Img()/255)
    #cv2.waitKey(0)
    #存储，不要映射回去[0,1]
   # cv2.imwrite(r'.\TestDate\Images\000004_noise.jpg',I.addNoise_Img())


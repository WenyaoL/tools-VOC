import DateAugmentLabelImg.ImgParser as ImgP
import DateAugmentLabelImg.LabelParser as LabelP
import os
import cv2
import time
from tqdm import tqdm


class DataAugmentVOC:
    def __init__(self,rootpath):
        '''
            会在数据集更目录下生成俩个文件夹，一个存储标签文件，一个存储图片
        :param rootpath:
        '''
        self.rootpath = rootpath
        self.Xmlpath = os.path.join(self.rootpath,'Annotations')
        self.Imgpath = os.path.join(self.rootpath,'JPEGImages')
        self.imgP = ImgP.ImgParser()    #图片解析器
        self.labP = LabelP.LabelParser()    #标签解析器

        self.save_xmlpath = os.path.join(rootpath,"change_Annotations")
        self.save_imgpath = os.path.join(rootpath, "change_JPEGImages")

        if not os.path.exists(self.save_imgpath):
            os.mkdir(self.save_imgpath)
        if not os.path.exists(self.save_xmlpath):
            os.mkdir(self.save_xmlpath)

        self.ImgPathlist = self._getImgPathlist()
        self.XMLPathlist = self._getXMLPathlist()

    def _getImg(self):
        return os.listdir(self.Imgpath)
    def _getImgPathlist(self):
        return [os.path.join(self.Imgpath,img) for img in os.listdir(self.Imgpath)]

    def _getXML(self):
        return os.listdir(self.Xmlpath)
    def _getXMLPathlist(self):
        return [os.path.join(self.Xmlpath,xml) for xml in os.listdir(self.Xmlpath)]


    def addNoise(self):
        '''
            对VOC数据集的所有图片添加高斯噪音，并复制一份label文件
        :return:
        '''
        start = time.time()
        count = 0
        for img, xml in tqdm(zip(self.ImgPathlist, self.XMLPathlist)):
            count +=1
            self.imgP.setImg(img)
            cv2.imwrite(self.save_imgpath+"\\noise"+str(count)+".jpg",
                        self.imgP.addNoise_Img(),
                        [int(cv2.IMWRITE_JPEG_QUALITY), 95]
                        )
            self.labP.setXML(xml)
            self.labP.copyXML(save_path=self.save_xmlpath,newname="noise_"+str(count)+".xml")
        end = time.time()
        print('A total of {} noise images are generated,a total of {}s'.format(str(count),end-start))

    def changeLight(self,r=None):
        '''
            对VOC数据集的所有图片调节亮度，并复制一份label文件
        :param r: 亮化程度
        :return:
        '''

        start = time.time()
        count = 0
        for img, xml in tqdm(zip(self.ImgPathlist, self.XMLPathlist)):
            count +=1
            self.imgP.setImg(img)
            cv2.imwrite(self.save_imgpath+"\\change_light_"+str(count)+".jpg",
                        self.imgP.changeLight_Img(r=r),
                        [int(cv2.IMWRITE_JPEG_QUALITY), 95]
                        )

            self.labP.setXML(xml)
            self.labP.copyXML(self.save_xmlpath,
                              "change_light_"+str(count)+".xml"
                              )
        end = time.time()
        print('A total of {} changeLight images are generated,a total of {}s'.format(str(count),end-start))

    def rotate(self,angle=5, scale=1.):
        '''
            对VOC数据集的数据进行旋转，生成新的旋转图片和新的label文件

        :param angle: 旋转角度
        :param scale:
        :return:
        '''
        start = time.time()
        count = 0
        for img, xml in tqdm(zip(self.ImgPathlist, self.XMLPathlist)):
            count += 1
            self.imgP.setImg(img)
            self.labP.setXML(xml)
            rot_img, rot_mat = self.imgP.rotate_Img(angle=angle, scale=scale)

            cv2.imwrite(self.save_imgpath + "\\rotate_" + str(count) + ".jpg",
                        rot_img,
                        [int(cv2.IMWRITE_JPEG_QUALITY), 95]
                        )

            self.labP.rotate_Object(rot_mat,
                                    w=rot_img.shape[0],
                                    h=rot_img.shape[1],
                                    c=rot_img.shape[2],
                                    save_path = self.save_xmlpath + "\\rotate_" + str(count) + ".xml",
                                    folder_name='VOC'
                                    )
        end = time.time()
        print('A total of {} change_rotate images are generated,a total of {}s'.format(str(count),end-start))

    def filp(self,filp=1):
        '''
            图片反转，默认水平反转
        :param filp:
        :return:
        '''
        start = time.time()
        count = 0
        for img, xml in tqdm(zip(self.ImgPathlist, self.XMLPathlist)):
            count += 1
            self.imgP.setImg(img)
            self.labP.setXML(xml)
            filp_img = self.imgP.filp_img(filp=filp)
            cv2.imwrite(self.save_imgpath + "\\filp_" + str(count) + ".jpg",
                        filp_img,
                        [int(cv2.IMWRITE_JPEG_QUALITY), 95]
                        )
            self.labP.reverse_Object(filp=filp, save_path=self.save_xmlpath + "\\filp_" + str(count) + ".xml")
        end = time.time()
        print('A total of {} filp images are generated,a total of {}s'.format(str(count),end-start))

if __name__ == '__main__':
    start = time.time()
    V = DataAugmentVOC(rootpath=r'.\TestDate\VOC')
    V.addNoise()
    V.changeLight()
    V.rotate(angle=15)
    V.filp(filp=1)
    end =time.time()
    print("total of {}".format(end-start))
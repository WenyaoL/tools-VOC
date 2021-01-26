import DateAugmentLabelImg.ImgParser as ImgP
import DateAugmentLabelImg.LabelParser as LabelP
import os
import cv2
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor,wait




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

    def _call(self, imgcallback,xmlcallback, **kwargs):

        def imgoperate(callback, **kwargs):
            filename = kwargs.pop('filename')
            count = 0
            for img in tqdm(self.ImgPathlist):
                count += 1
                self.imgP.setImg(img)
                path = os.path.join(self.save_imgpath,filename + str(count) + ".jpg")

                cv2.imwrite(path,
                            callback(**kwargs['imgconfig']),
                            [int(cv2.IMWRITE_JPEG_QUALITY), 95]
                            )

        def xmlorerate(callback,**kwargs):
            filename = kwargs.pop('filename')
            count = 0
            for xml in tqdm(self.XMLPathlist):
                count += 1
                self.labP.setXML(xml)
                kwargs['xmlconfig']['save_path'] = os.path.join(self.save_xmlpath, filename+str(count)+".xml")
                callback(**kwargs['xmlconfig'])


        executor = ThreadPoolExecutor(max_workers=2)
        f_list = []
        f1 = executor.submit(imgoperate,imgcallback,**kwargs)
        f2 = executor.submit(xmlorerate,xmlcallback,**kwargs)
        f_list.append(f1)
        f_list.append(f2)
        wait(f_list)


    def setSave_xmlpath(self,path):
        self.save_xmlpath = path

    def setSave_imgpath(self,path):
        self.save_imgpath = path

    def addNoise(self):
        '''
            对VOC数据集的所有图片添加高斯噪音，并复制一份label文件
        :return:
        '''
        # 呼叫_call方法多线程执行
        self._call(imgcallback= self.imgP.addNoise_Img,
                   xmlcallback= self.labP.copyXML,
                   filename="noise_",
                   imgconfig={},
                   xmlconfig={}
                   )

    def changeLight(self,r=None):
        '''
            对VOC数据集的所有图片调节亮度，并复制一份label文件
        :param r: 亮化程度
        :return:
        '''

        #呼叫_call方法多线程执行
        self._call(imgcallback=self.imgP.changeLight_Img,
                   xmlcallback=self.labP.copyXML,
                   filename="changeLight_",
                   imgconfig={
                       'r': r
                   },
                   xmlconfig={}
                   )

    def changeHsv(self,hub=.1, sat=.1, val=.1):
        '''
                hsv调整
            :param hue_delta:色调变化比例
            :param sat_mult:饱和度变化比例
            :param val_mult:明度变化比例
            :return:
        '''
        # 呼叫_call方法多线程执行
        self._call(imgcallback=self.imgP.hsv_transform,
                   xmlcallback=self.labP.copyXML,
                   filename="changeHsv_",
                   imgconfig={
                       'hue_delta' : hub,
                       'sat_mult' : sat,
                       'val_mult' : val
                   },
                   xmlconfig={}
                   )

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
                                    save_path = self.save_xmlpath + "\\rotate_" + str(count) + ".xml"
                                    )
        end = time.time()
        print('A total of {} change_rotate images are generated,a total of {}s'.format(str(count),end-start))

    def filp(self,filp=1):
        '''
            图片反转，默认水平反转
        :param filp:
        :return:
        '''
        # 呼叫_call方法多线程执行
        self._call(imgcallback=self.imgP.filp_img,
                   xmlcallback=self.labP.reverse_Object,
                   filename="filp_",
                   imgconfig={'filp':1},
                   xmlconfig={'filp':1}
                   )

if __name__ == '__main__':
    start = time.time()
    V = DataAugmentVOC(rootpath=r'.\TestDate\VOC')

    #V.setSave_imgpath(r'.\TestDate\VOC\JPEGImages')
    #V.setSave_xmlpath(r'.\TestDate\VOC\Annotations')
    V.changeHsv(hub=30,sat=1.2, val=1.2)  #hub 0~180   sat 0~2   val 0~2
    V.addNoise()
    V.changeLight()
    V.rotate(angle=5)
    V.filp(filp=1)
    end =time.time()
    print("total of {}".format(end-start))
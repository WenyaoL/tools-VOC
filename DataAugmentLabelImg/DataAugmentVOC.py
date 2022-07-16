import DataAugmentLabelImg.ImgParser as ImgP
import DataAugmentLabelImg.LabelParser as LabelP
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

        self.save_xmlpath = os.path.join(rootpath, "change_Annotations")
        self.save_imgpath = os.path.join(rootpath, "change_JPEGImages")

        if not os.path.exists(self.save_imgpath):
            os.mkdir(self.save_imgpath)
        if not os.path.exists(self.save_xmlpath):
            os.mkdir(self.save_xmlpath)

        #图片和标签文件的list
        self.sourceMap = self._getSourceMap()




    def _getSourceMap(self):

        #求文件名和后缀
        img_dict = dict([os.path.splitext(img_name) for img_name in os.listdir(self.Imgpath)])
        xml_dict = dict([os.path.splitext(xml_name) for xml_name in os.listdir(self.Xmlpath)])
        #求文件名交集,
        u_list = list(set(img_dict.keys()).intersection(set(xml_dict.keys())))

        #拼接成文件名
        img_list = [name+img_dict[name] for name in sorted(u_list)]
        xml_list = [name+xml_dict[name] for name in sorted(u_list)]
        return list(zip(img_list,xml_list))


    def _call(self, **kwargs):

        def imgoperate(callback, **kwargs):
            prefix = kwargs['prefix']
            for img,_ in tqdm(self.sourceMap):
                #图片路径
                img_path = os.path.join(self.Imgpath,img)
                self.imgP.setImg(img_path)

                #保存图片路径
                save_path = os.path.join(self.save_imgpath,prefix + img)

                #增强
                cv2.imwrite(save_path,
                            callback(**kwargs['imgconfig']),
                            [int(cv2.IMWRITE_JPEG_QUALITY), 95]
                            )

        def xmlorerate(callback,**kwargs):
            prefix = kwargs['prefix']

            for _,xml in tqdm(self.sourceMap):
                # 标签路径
                xml_path = os.path.join(self.Xmlpath, xml)
                self.labP.setXML(xml_path)

                #设置标签保存路径和保存名称
                kwargs['xmlconfig']['save_path'] = self.save_xmlpath
                kwargs['xmlconfig']['save_name'] = prefix+xml

                callback(**kwargs['xmlconfig'])


        executor = ThreadPoolExecutor(max_workers=2)
        f_list = []
        f1 = executor.submit(imgoperate,kwargs['imgcallback'],**kwargs)
        f2 = executor.submit(xmlorerate,kwargs['xmlcallback'],**kwargs)
        f_list.append(f1)
        f_list.append(f2)

        #两线程都结束
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
                   prefix="noise_",
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
                   prefix="changeLight_",
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
                   prefix="changeHsv_",
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

        for img, xml in tqdm(self.sourceMap):
            #图片和标签路径
            img_path = os.path.join(self.Imgpath,img)
            xml_path = os.path.join(self.Xmlpath,xml)
            #设置
            self.imgP.setImg(img_path)
            self.labP.setXML(xml_path)
            #旋转图片
            rot_img, rot_mat = self.imgP.rotate_Img(angle=angle, scale=scale)

            #保存旋转图片
            cv2.imwrite(os.path.join(self.save_imgpath, "rotate_"+img),
                        rot_img,
                        [int(cv2.IMWRITE_JPEG_QUALITY), 95]
                        )
            #旋转标签
            self.labP.rotate_Object(rot_mat,
                                    w=rot_img.shape[0],
                                    h=rot_img.shape[1],
                                    c=rot_img.shape[2],
                                    save_path=self.save_xmlpath,
                                    save_name="rotate_"+xml
                                    )



    def filp(self,filp=1):
        '''
            图片反转，默认水平反转
        :param filp:
        :return:
        '''
        # 呼叫_call方法多线程执行
        self._call(imgcallback=self.imgP.filp_img,
                   xmlcallback=self.labP.reverse_Object,
                   prefix="filp_",
                   imgconfig={'filp':1},
                   xmlconfig={'filp':1}
                   )


if __name__ == '__main__':
    start = time.time()
    V = DataAugmentVOC(rootpath=r'..\TestData\VOC')

    #V.setSave_imgpath(r'.\TestDate\VOC\JPEGImages')
    #V.setSave_xmlpath(r'.\TestDate\VOC\Annotations')
    V.changeHsv(hub=30,sat=1.2, val=1.2)  #hub 0~180   sat 0~2   val 0~2
    V.addNoise()
    V.changeLight()
    V.rotate(angle=5)
    V.filp(filp=1)
    end =time.time()
    print("total of {}".format(end-start))
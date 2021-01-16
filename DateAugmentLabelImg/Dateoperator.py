import os
from tqdm import tqdm
import cv2
import time
import DateAugmentLabelImg.ImgParser as ImgP
import DateAugmentLabelImg.LabelParser as LabelP


class DataOperator:
    def __init__(self,rootpath):
        self.rootpath = rootpath
        self.imgP = ImgP.ImgParser()    #图片解析器
        self.labP = LabelP.LabelParser()    #标签解析器

        self.Xmlpath = os.path.join(self.rootpath, 'Annotations')
        self.Imgpath = os.path.join(self.rootpath, 'JPEGImages')

        self.save_xmlpath = os.path.join(rootpath, "resize_Annotations")
        self.save_imgpath = os.path.join(rootpath, "resize_JPEGImages")

        if not os.path.exists(self.save_imgpath):
            os.mkdir(self.save_imgpath)
        if not os.path.exists(self.save_xmlpath):
            os.mkdir(self.save_xmlpath)


    def _getImgPathlist(self):
        return [os.path.join(self.Imgpath,img) for img in os.listdir(self.Imgpath)]

    def _getXMLPathlist(self):
        return [os.path.join(self.Xmlpath,xml) for xml in os.listdir(self.Xmlpath)]

    def _getImgName(self):
        return [img for img in os.listdir(self.Imgpath)]

    def _getXmlName(self):
        return [xml for xml in os.listdir(self.Xmlpath)]

    def resize_dataset(self,*args):
        width = args[0]
        hight = args[-1]
        start = time.time()
        count = 10584
        for img, xml in tqdm(zip(self._getImgPathlist(), self._getXMLPathlist())):
            count += 1

            self.imgP.setImg(img)
            self.imgP.resize_Img(width,hight)
            cv2.imwrite(self.save_imgpath+"\\resize_"+str(count)+".jpg",
                        self.imgP.resize_Img(width,hight),
                        [int(cv2.IMWRITE_JPEG_QUALITY), 95]
                        )

            self.labP.setXML(xml)
            self.labP.changeImg_size(save_path=self.save_xmlpath,newsize=(width,hight))

        end = time.time()
        print('A total of {} resize images are generated,a total of {}s'.format(str(count), end - start))


if __name__ == '__main__':
    operator = DataOperator(rootpath=r'F:\alldate\school_data\HSV_SAVE')
    operator.resize_dataset(460*2,345*2)


import numpy as np
import os
import cv2
from lxml import objectify
import lxml.etree as ET


class LabelParser:
    def __init__(self, XMLPath=None):
        self.XMLPath = XMLPath
        if XMLPath != None:
            self.XMLName = os.path.split(self.XMLPath)[-1]
            self.tree = tree = ET.parse(XMLPath)
            self.root = tree.getroot()

    def setXML(self,path):
        self.XMLPath = path
        self.XMLName = os.path.split(self.XMLPath)[-1]
        self.tree = tree = ET.parse(self.XMLPath)
        self.root = tree.getroot()

    def getObject(self,XMLpath =None):
        '''
            默认从当前文件读取
            从xml文件中提取bounding box信息, 格式为[[ name,x_min, y_min, x_max, y_max]]
        :param XMLpath: 指定读取文件
        :return: [[ name,x_min, y_min, x_max, y_max]]
        '''

        if XMLpath == None:
            XMLpath = self.XMLPath

        objs = self.root.findall('object')
        coords = list()
        for obj in objs:
            name = obj.find('name').text
            box = obj.find('bndbox')
            x_min = int(box[0].text)
            y_min = int(box[1].text)
            x_max = int(box[2].text)
            y_max = int(box[3].text)
            coords.append([name,x_min, y_min, x_max, y_max])
        return coords

    def changeObject(self):
        pass

    def reverse_Object(self,filp=1,save_path=None):
        '''
            对label文件中的所有目标对象进行反转,默认存储在原文件
        :param filp: 反转方式（1：水平，0：垂直）
        :param save_path: 新的保存路径
        :return:
        '''
        if os.path.isdir(save_path):
            save_path = os.path.join(save_path, self.XMLName.split('.')[0] + "_reverse_Object.xml")

        if filp==1:
            width = self.root.find('.//size/width')
            xmin = self.root.findall('.//bndbox/xmin')
            xmax = self.root.findall('.//bndbox/xmax')
            for index in range(len(xmin)):
                xmin[index].text = str(int(width.text) - int(xmin[index].text))
                xmax[index].text = str(int(width.text) - int(xmax[index].text))


        if filp==0:
            height = self.root.find('.//size/height')
            ymin = self.root.findall('.//bndbox/ymin')
            ymax = self.root.findall('.//bndbox/ymax')
            for index in range(len(ymin)):
                ymin[index].text = str(int(height.text) - int(ymin[index].text))
                ymax[index].text = str(int(height.text) - int(ymax[index].text))

        self.tree.write(save_path, encoding="utf-8", xml_declaration=True)

    def rotate_Object(self, rot_mat,w,h,c,save_path =None, folder_name=None):
        '''
            根据仿射变换矩阵来对对象标签进行转换,
            默认保存路径为原文件，也可以指定新的
            路径

        :param rot_mat:仿射变换矩阵
        :param save_path:新的保存路径
        :return:
        '''


        if save_path is None:
            save_path =self.XMLPath

        if os.path.isdir(save_path):
            save_path = os.path.join(save_path, self.XMLName.split('.')[0] + "_reverse_Object.xml")

        #更改图片大小
        self.root.find('size/width').text = str(w)
        self.root.find('size/height').text = str(h)
        self.root.find('size/depth').text = str(c)

        #更改Object坐标
        xmins = self.root.findall('object/bndbox//xmin')
        ymins = self.root.findall('object/bndbox//ymin')
        xmaxs = self.root.findall('object/bndbox//xmax')
        ymaxs = self.root.findall('object/bndbox//ymax')
        for x_min, y_min, x_max, y_max in zip(xmins, ymins, xmaxs, ymaxs):
            #转换
            xmin = int(x_min.text)
            ymin = int(y_min.text)
            xmax = int(x_max.text)
            ymax = int(y_max.text)
            point1 = np.dot(rot_mat, np.array([(xmin + xmax) / 2, ymin, 1]))
            point2 = np.dot(rot_mat, np.array([xmax, (ymin + ymax) / 2, 1]))
            point3 = np.dot(rot_mat, np.array([(xmin + xmax) / 2, ymax, 1]))
            point4 = np.dot(rot_mat, np.array([xmin, (ymin + ymax) / 2, 1]))
            # 合并np.array
            concat = np.vstack((point1, point2, point3, point4))
            # 改变array类型
            concat = concat.astype(np.int32)
            # 得到旋转后的坐标
            rx, ry, rw, rh = cv2.boundingRect(concat)
            x_min.text = str(rx)
            y_min.text = str(ry)
            x_max.text = str(rx + rw)
            y_max.text = str(ry + rh)

        self.tree.write(save_path, encoding="utf-8", xml_declaration=True)



    def copyXML(self, save_path=None, newname=None):
        '''
            复制当前XML文件到指定的新目录下

        :param save_path: 保存文件或目录的路径
        :param newname: 文件的新名字
        :return:
        '''

        if os.path.isdir(save_path):
            save_path = os.path.join(save_path, newname)

        path = self.root.find('path')
        if path:
            path.text = save_path
        self.tree.write(save_path, encoding="utf-8", xml_declaration=True)

    def deleteObject(self, ObjectName, save_path=None):
        '''
            删除标签文件里的对应对象，默认写回到原文件，如果
            指定新的保存路径，信息将保存到新的文件中

        :param ObjectName: 删除的对象名
        :param save_path: 指定新的保存路径
        :return:
        '''
        if save_path is None:
            save_path =self.XMLPath

        if os.path.isdir(save_path):
            save_path = os.path.join(save_path, self.XMLName.split('.')[0] + "_change.xml")

        objs = self.root.findall('object')
        for obj in objs:
            objname = obj.find('name').text
            if objname  ==  ObjectName:
                self.root.remove(obj)
        if save_path !=None:
            self.tree.write(save_path, encoding="utf-8", xml_declaration=True)
        else:
            self.tree.write(self.XMLPath, encoding="utf-8", xml_declaration=True)


    def change_ObjectName(self, oldName, newName, save_path=None):
        '''
            更改当前xml文件的对象名，默认写回原文件，也可以通过
            NewPath指定新的保存路径

        :param oldName: 旧的对象名
        :param newName: 新的对象名
        :param save_path: 新的文件保存路径
        :return:
        '''
        if save_path is None:
            save_path =self.XMLPath
        if os.path.isdir(save_path):
            save_path = os.path.join(save_path, self.XMLName.split('.')[0] + "_change.xml")

        objs = self.root.findall('object')
        for obj in objs:
            name = obj.find('name')
            if name.text == oldName:
                name.text = newName

        if save_path !=None:
            self.tree.write(save_path, encoding="utf-8", xml_declaration=True)
        else:
            self.tree.write(self.XMLPath, encoding="utf-8", xml_declaration=True)

    def getImg_size(self):
        '''
            返回标签图片的宽，高，通道
        :return: width,height,channel
        '''
        width = self.root.find('size/width').text
        height = self.root.find('size/height').text
        channel = self.root.find('size/depth').text
        return width,height,channel


    def changeImg_size(self, newsize, save_path=None):
        '''
            文件默认存储路径为原文件，可以通过NewPath指定
            新的保存路径

            更改标签文件中图片大小数值，并且对应的对象框
            也得到相应的改变。
        :param newsize: 图片新大小
        :param save_path: 标签文件存储路径
        :return:
        '''
        if save_path is None:
            save_path =self.XMLPath
        if os.path.isdir(save_path):
            save_path = os.path.join(save_path, self.XMLName.split('.')[0] + "_changeImg_size.xml")

        width = self.root.find('size/width')
        oldwidth = float(width.text)
        width.text = str(newsize[0])
        changerate_x = newsize[0] / oldwidth

        height = self.root.find('size/height')
        oldheight = float(height.text)
        height.text = str(newsize[-1])
        changerate_y = newsize[-1] / oldheight

        xmins = self.root.findall('object/bndbox//xmin')
        ymins = self.root.findall('object/bndbox//ymin')
        xmaxs = self.root.findall('object/bndbox//xmax')
        ymaxs = self.root.findall('object/bndbox//ymax')
        for xmin, ymin, xmax, ymax in zip(xmins, ymins, xmaxs, ymaxs):
            xmin.text = str(int(int(xmin.text) * changerate_x))
            ymin.text = str(int(int(ymin.text) * changerate_y))
            xmax.text = str(int(int(xmax.text) * changerate_x))
            ymax.text = str(int(int(ymax.text) * changerate_y))

        if save_path != None:
            self.tree.write(save_path, encoding="utf-8", xml_declaration=True)
        else:
            self.tree.write(self.XMLPath, encoding="utf-8", xml_declaration=True)



if __name__ == '__main__':
    #加载
    paser = LabelParser(r'.\TestDate\label\000004.xml')
    #改变图片大小
    paser.changeImg_size([1222,1250],r'.\TestDate\label')
    #获取图片size
    print(paser.getImg_size())
    #改变对象名，默认写回加载文件，也可以指定新的路径。
    paser.change_ObjectName('car', 'bigcar',save_path='.\TestDate\label')

    #删除指定Object
    #paser.deleteObject('star')

    #获得对象数据
    print(paser.getObject())

    #对label里面的框做镜像反转,并指定新保存路径
    paser.reverse_Object(filp=0, save_path='.\TestDate\label')
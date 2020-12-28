# encoding:utf-8
import os
import xml.etree.ElementTree as ET


#nowDir = os.getcwd()  # 得到进程当前工作目录
#fileList = os.listdir(nowDir)  # 得到进程当前工作目录中的所有文件名称列表

Dir = r"F:\alldate\VOC2007\Annotations"
fileList = os.listdir(Dir)
StoreDir=r"F:\alldate\VOC2007\Annotations"        #存储目录
for fileName in fileList:  # 获取文件列表中的文件
    if fileName.endswith("xml"):
        print(fileName)
        tree = ET.parse(os.path.join(Dir,fileName))
        root = tree.getroot()
        for child in root:
            if child.tag=="folder":
                child.text="VOC2007"
            if child.tag=="path":
                child.text="/root/object_det_test/VOCdevkit/VOC2007/JPEGImages/"+fileName.split('.')[0]+".jpg"
            if child.tag == "filename":
                child.text = fileName.split('.')[0]+".jpg"
        tree.write(os.path.join(StoreDir,fileName))  # 保存修改后的XML文件








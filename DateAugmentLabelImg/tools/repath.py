# encoding:utf-8
import os
import xml.etree.ElementTree as ET
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='修改标签名')
    parser.add_argument('--xmlpath', dest='xmlpath', help='xml file path',
                        type=str, required=True)
    parser.add_argument('--storepath', dest='store', help='存储位置，默认覆盖',
                        type=str)
    args = parser.parse_args()
    return args

#nowDir = os.getcwd()  # 得到进程当前工作目录
#fileList = os.listdir(nowDir)  # 得到进程当前工作目录中的所有文件名称列表
if __name__ == '__main__':
    args = parse_args()
    fileList = os.listdir(args.xmlpath)
    if args.store == None:
        StoreDir=args.xmlpath       #存储目录
    else:
        StoreDir = args.store

    for fileName in fileList:  # 获取文件列表中的文件
        if fileName.endswith("xml"):
            print(fileName)
            tree = ET.parse(os.path.join(args.xmlpath,fileName))
            root = tree.getroot()
            for child in root:
                if child.tag=="folder":
                    child.text="VOC2007"
                if child.tag=="path":
                    child.text="/root/object_det_test/VOCdevkit/VOC2007/JPEGImages/"+fileName.split('.')[0]+".jpg"
                if child.tag == "filename":
                    child.text = fileName.split('.')[0]+".jpg"
            tree.write(os.path.join(StoreDir,fileName))  # 保存修改后的XML文件







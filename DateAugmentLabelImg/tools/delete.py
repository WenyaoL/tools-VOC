import os
import argparse
from tqdm import tqdm
'''
    删除没打标签的图片
'''
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--imgpath', type=str, required=True)
    parser.add_argument('--xmlpath', type=str, required=True)
    return parser.parse_known_args()

if __name__ == '__main__':
    args,_ = parse_args()
    xmllist = os.listdir(args.xmlpath) #该文件夹下所有的文件（包括文件夹）
    imglist = os.listdir(args.imgpath)
    tp = ".xml"      #要匹配标签文件的后缀


    for imgname in tqdm(imglist):
        filename = os.path.splitext(imgname)[0] + tp  # 匹配文件名
        if filename not in xmllist:           #如果没有对应匹配文件，就删除
            os.remove(os.path.join(args.imgpath,imgname))
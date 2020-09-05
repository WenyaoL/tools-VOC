import os
import cv2
import  xml.dom.minidom
from tqdm import tqdm

'''
    脚本来自：https://blog.csdn.net/ptgood/article/details/86997486
    在此基础上做了些bug的修复
'''
image_path=r".\TestDate\VOC\change_JPEGImages"
annotation_path=r".\TestDate\VOC\change_Annotations"
save_path =r'.\TestDate\VOC\vision2'

img_names = os.listdir(image_path)
xml_names = os.listdir(annotation_path)
for img_n, xml_n in tqdm(zip(img_names, xml_names)):
    img_path =os.path.join(image_path, img_n)
    xml_path =os.path.join(annotation_path,xml_n)
    img = cv2.imread(img_path)
    if img is None:
        pass
    try:
        dom = xml.dom.minidom.parse(xml_path)
    except:
        continue
    root = dom.documentElement
    objects=dom.getElementsByTagName("object")
    for object in objects:
        bndbox = object.getElementsByTagName('bndbox')[0]
        xmin = bndbox.getElementsByTagName('xmin')[0]
        ymin = bndbox.getElementsByTagName('ymin')[0]
        xmax = bndbox.getElementsByTagName('xmax')[0]
        ymax = bndbox.getElementsByTagName('ymax')[0]
        xmin_data=int(xmin.childNodes[0].data)
        ymin_data=int(ymin.childNodes[0].data)
        xmax_data=int(xmax.childNodes[0].data)
        ymax_data=int(ymax.childNodes[0].data)
        label_name=object.getElementsByTagName('name')[0].childNodes[0].data
        cv2.rectangle(img,(xmin_data,ymin_data),(xmax_data,ymax_data),(55,255,155),1)
        cv2.putText(img,label_name,(xmin_data,ymin_data),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),1)
    flag=0
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    flag=cv2.imwrite(os.path.join(save_path,img_n),img)
    if not (flag):
        print(img_n,"error")
print("all done ====================================")
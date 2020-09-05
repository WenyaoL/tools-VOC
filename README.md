# VOCDateAugment
目的：对VOC数据集的对象检测的数据进行数据增强。
**如果能帮到您请给本人一颗⭐，拜托了！！！！！**
### visualiztion模块

这个模块是脚本，主要功能是通过图片和其label文件，生成带bboxs的图片。效果如下图片

![image](https://github.com/Mygithub-Yao/tools-VOC/blob/master/DateAugmentLabelImg/TestDate/VOC/vision/000004.jpg)

### ImgParser模块

里面有class ImgParser类，类提供了5个图片数据增强的功能，分别是：加噪音（高斯），反转，旋转，平移，光度随机调节。

```python
def addNoise_Img(self, img=None):
def filp_img(self, img=None, filp=1):
def rotate_Img(self, img=None, angle=5, scale=1.):
def shift_Img(self,x,y,img=None):
def changeLight_Img(self, img=None):
```

功能展示：

```python
if __name__ == '__main__':
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
    #存储，不要映射回去[0,1]
   # cv2.imwrite(r'.\TestDate\Images\000004_noise.jpg',I.addNoise_Img())
```

![image](https://github.com/Mygithub-Yao/tools-VOC/blob/master/DateAugmentLabelImg/TestDate/29.png)

### LabelParser模块

此功能模块主要是对标签进行处理的，里面包含一个class LabelParser的类，并且提供一下功能：

```python
#从xml文件中提取bounding box信息, 格式为[[ name,x_min, y_min, x_max, y_max]]
def getObject(self,XMLpath =None):

#对label文件中的所有目标对象进行反转,默认存储在原文件
def reverse_Object(self,filp=0,save_path=None):

#根据仿射变换矩阵来对对象标签进行转换,默认保存路径为原文件，也可以指定新的路径
def rotate_Object(self, rot_mat,w,h,c,save_path =None, folder_name=None):

#复制当前XML文件到指定的新目录下
def copyXML(self, save_path, newname):

#删除标签文件里的对应对象，默认写回到原文件，如果指定新的保存路径，信息将保存到新的文件中
def deleteObject(self, ObjectName, save_path=None):

#更改当前xml文件的对象名，默认写回原文件，也可以通过NewPath指定新的保存路径
def change_ObjectName(self, oldName, newName, save_path=None):

#返回标签图片的宽，高，通道
def getImg_size(self):

#文件默认存储路径为原文件，可以通过NewPath指定新的保存路径
def changeImg_size(self, newsize, save_path=None):

#设置要解析的标签文件
def setXML(self,path):
```

一个小示例：

```python
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
```

### DataAugmentVOC模块

此模块提供简易的批处理数据增强，通过新建类DataAugmentVOC来提供批量VOC数据集的数据增强。

提供以下功能：

```python
#图片反转，默认水平反转
def filp(self,filp=1):

#对VOC数据集的数据进行旋转，生成新的旋转图片和新的label文件
def rotate(self,angle=5, scale=1.):

#对VOC数据集的所有图片调节亮度，并复制一份label文件，r指定亮化值
def changeLight(self,r=None):

#对VOC数据集的所有图片添加高斯噪音，并复制一份label文件
def addNoise(self):
```

小示例：

```python
if __name__ == '__main__':
    start = time.time()
    V = DataAugmentVOC(rootpath=r'.\TestDate\VOC')
    V.addNoise()
    V.changeLight()
    V.rotate(angle=15)
    V.filp(filp=1)
    end =time.time()
    print("total of {}".format(end-start))
```

生成结果保存在新文件夹：

![image](https://github.com/Mygithub-Yao/tools-VOC/blob/master/DateAugmentLabelImg/TestDate/30.png)

结果图片：（部分）

![31](https://github.com/Mygithub-Yao/tools-VOC/blob/master/DateAugmentLabelImg/TestDate/31.png)

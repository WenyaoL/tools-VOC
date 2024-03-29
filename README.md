# 对PASCAL VOC 数据集进行数据增强

### 常见问题

**在执行脚本时，无生成完全的数据集（出现缺失问题）（已经修复）**

解决办法：去除原数据集中没有打标签的图片和没图片的标签，并确保图片和标签一一对应的关系，（即无多余的标签和多余的图片，并且文件名一致）

**生成的数据和文件无法对应（已经修复）**

解决办法：跟上面的一样。或者到window系统下运行脚本。问题出现的主要原因：文件排序不一致，或者出现缺失。

**旋转的后的框无法完全覆盖物品问题（已经修复）**

问题原因：物体自身形状问题，导致生成的新的框无法完全覆盖物体。

解决办法：可以修改**tools-VOC/DateAugmentLabelImg/LabelParser.py**下的116~129行之间的代码，修改代码中的除数4（范围：2~max）。以调整框的收缩，修改到符合数据集的要求。

****



### 项目核心处理逻辑

如想查看或借鉴图片和标签操作，请核心看：

- **tools-VOC/DateAugmentLabelImg/LabelParser.py**
- **tools-VOC/DateAugmentLabelImg/ImgParser.py**





### 1.GitHub仓库位置

目的：对VOC数据集的对象检测的数据进行数据增强。

https://github.com/Mygithub-Yao/tools-VOC

### 2.项目目录解析

```
DataAugmentLabelImg   //增强功能代码
show_picture         //readme.md文件用的的图片
TestData			//测试数据集
Augment_scripy.py          //脚本代码
README.md
```

### 3.使用script对数据集增强

#### 3.1获取帮助

```
python Augment_script.py -h
```

显示结果：

```
usage: Augment_script.py [-h] --root ROOT_PATH [--xmlpath XMLPATH] [--imgpath IMGPATH] [--hub HUB] [--sat SAT] [--val VAL] [--rotate ROTATE] [--Noise] [--changeLight] [--filp] [--mul_processs]

aug dataset

optional arguments:
  -h, --help         show this help message and exit
  --root ROOT_PATH   dataset root path
  --xmlpath XMLPATH  自定义xml文件位置,默认是数据集根目录下生成新的文件夹
  --imgpath IMGPATH  自定义img文件位置,默认是数据集根目录下生成新的文件夹
  --hub HUB          hub调节,范围0~180
  --sat SAT          饱和度变化比例调节,范围0~2
  --val VAL          明度变化比例调节,范围0~2
  --rotate ROTATE    旋转角度
  --Noise            添加高斯噪音
  --changeLight      随机光度调节
  --filp             水平翻转
  --mul_processs     启用多进程处理
```

#### 3.2增强例子

**hvs调节**

```shell
python Augment_script.py --hub=30 --sat=1.2 --val=1.2  --root=./TestData/VOC
```

**随机亮度调节**

```shell
python Augment_script.py --changeLight --root=./TestData/VOC
```

**高斯噪点**

```shell
python Augment_script.py --Noise --root=./TestData/VOC
```

**旋转指定角度**

```shell
python Augment_script.py --rotate=10 --root=./TestData/VOC
```

**水平翻转**

```shell
python Augment_script.py --filp --root=./TestData/VOC
```

**结果展示：**

![image](./show_picture/75.jpg)

#### 3.3可视测试
**使用visualization脚本**

查看使用参数，具体效果可以查看TestData/VOC目录下的vis_img文件夹
```
python visualization.py  -h
```





### 4.其他工具脚本

在**DataAugmentLabellmg/tools**文件夹下面









### 项目进度

- 2020/9/4 项目初始化
- 2021/8/6 项目放弃维护，本项目存在设计问题，在标签文件和图片没严格一致对应时，出现数据生成发生错误和丢失。
- 2021/12 项目设为私有仓库，因为项目存在问题，免得造成不必要的麻烦，将项目设为私有（star清空了）
- 2022/6/3 项目重新维护，并**修复常见问题**

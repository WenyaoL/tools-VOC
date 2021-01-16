from DateAugmentLabelImg.DataAugmentVOC import DataAugmentVOC
from DateAugmentLabelImg.multiprocessAug import multiprocessAug
import argparse
def parse_args():
    parser = argparse.ArgumentParser(description='aug dataset')
    parser.add_argument('--root', dest='root_path', help='dataset root path',required=True,
                        type=str)
    parser.add_argument('--xmlpath', dest='xmlpath', help='自定义xml文件位置,默认是数据集根目录下生成新的文件夹',
                        type=str)
    parser.add_argument('--imgpath', dest='imgpath', help='自定义img文件位置,默认是数据集根目录下生成新的文件夹',
                        type=str)
    parser.add_argument('--hub', dest='hub', help='hub调节,范围0~180',
                        type=int)
    parser.add_argument('--sat', dest='sat', help='饱和度变化比例调节,范围0~2',default=1,
                        type=float)
    parser.add_argument('--val', dest='val', help='明度变化比例调节,范围0~2',default=1,
                        type=float)
    parser.add_argument('--rotate', dest='rotate', help='旋转角度',
                        type=int)
    parser.add_argument('--Noise', dest='Noise', help='添加高斯噪音', default=False,
                        type=bool)
    parser.add_argument('--changeLight', dest='changeLight', help='随机光度调节', default=False,
                        type=bool)
    parser.add_argument('--filp', dest='filp', help='水平翻转', default=False,
                        type=bool)
    parser.add_argument('--mul_processs', dest='mul_processs', help='启用多进程处理', default=True,
                        type=bool)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()

    #use multiprocess
    if args.mul_processs is True:
        multiprocessAug(args)
    else:
        V = DataAugmentVOC(rootpath=args.root_path)
        if args.xmlpath is not None:
            V.setSave_xmlpath(args.xmlpath)
        if args.imgpath is not None:
            V.setSave_imgpath(args.imgpath)
        if args.hub is not None:
            V.changeHsv(hub=args.hub, sat=args.sat, val=args.val)  # hub 0~180   sat 0~2   val 0~2
        if args.rotate is not None:
            V.rotate(angle=args.rotate)
        if args.Noise is True:
            V.addNoise()
        if args.changeLight is True:
            V.changeLight()
        if args.filp is True:
            V.filp(filp=1)

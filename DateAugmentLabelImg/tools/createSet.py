import os
import random
import argparse

def parse_args():
    parser = argparse.ArgumentParser()


    parser.add_argument('--trainval', type=float, default=0.9)
    parser.add_argument('--train', type=int, default=0.7)

    parser.add_argument('--xmlfilepath', type=str, required=True)
    parser.add_argument('--txtsavepath', type=str, required=True)


    return parser.parse_known_args()

if __name__ == '__main__':
    args,_ = parse_args()
    trainval_percent = args.trainval  # 标注文件中训练验证所占的比例           (测试集：训练和验证集)
    train_percent = args.train  # 训练验证中训练所占的比例                  （验证集：训练集）
    xmlfilepath = args.xmlfilepath  # 标注文件的路径 ，格式为.xml的
    txtsavepath = args.txtsavepath  # 生成的各个txt存放的路径
    total_xml = os.listdir(xmlfilepath)
    print(total_xml)
    num = len(total_xml)
    list = range(num)
    tv = int(num * trainval_percent)
    tr = int(tv * train_percent)
    trainval = random.sample(list, tv)
    train = random.sample(trainval, tr)

    ftrainval = open(os.path.join(txtsavepath,'trainval.txt'), 'w')  # 用于写训练验证的序列
    ftest = open(os.path.join(txtsavepath,'test.txt'), 'w')
    ftrain = open(os.path.join(txtsavepath,'train.txt'), 'w')
    fval = open(os.path.join(txtsavepath,'val.txt'), 'w')

    for i in list:
        name = total_xml[i][:-4] + '\n'
        if i in trainval:
            ftrainval.write(name)
            if i in train:
                ftrain.write(name)
            else:
                fval.write(name)
        else:
            ftest.write(name)

    ftrainval.close()
    ftrain.close()
    fval.close()
    ftest.close()

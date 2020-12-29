import os
import argparse
from tqdm import tqdm
def parse_args():
    parser = argparse.ArgumentParser(description='rename for picture')
    parser.add_argument('--root', dest='root_path', help='dataset root path',
                        type=str)
    parser.add_argument('--clear_suffix', dest='clear_suffix', help='清洗符合后缀名的图片',
                        type=str)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    Dir = args.root_path
    count=0
    fileList = os.listdir(Dir)
    os.chdir(Dir)
    for filename in tqdm(fileList):
        if filename.split('.')[-1] == args.clear_suffix:
            os.remove(filename)
            count+=1
    print('总共删除%d张图片' % count)
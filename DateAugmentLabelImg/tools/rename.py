import os
import argparse
from tqdm import tqdm
def parse_args():
    parser = argparse.ArgumentParser(description='rename for picture')
    parser.add_argument('--root', dest='root_path', help='dataset root path',
                        type=str, required=True)
    parser.add_argument('--n', dest='num', help='位数',
                        type=int, required=True)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    Dir = args.root_path
    count=0
    fileList = os.listdir(Dir)
    os.chdir(Dir)
    for filename in tqdm(fileList):
        os.rename(filename, str(count).zfill(args.num)+'.'+filename.split('.')[-1])
        count+=1
    print('总共更名%d张图片' % count)
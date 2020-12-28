import os
'''
    删除没打标签的图片
'''
if __name__ == '__main__':
    path1 = r"F:\alldate\SHONG\Annotations"       #对比的文件夹（标签文件夹）
    path2 = r"F:\alldate\SHONG\JPEGImages"        #删除文件的文件夹（图片文件夹）
    filelist1 = os.listdir(path1) #该文件夹下所有的文件（包括文件夹）
    filelist2 = os.listdir(path2)
    tp = ".xml"      #要匹配标签文件的后缀


    for file2 in filelist2:
        filename = os.path.splitext(file2)[0] + tp  # 匹配文件名
        if filename not in filelist1:           #如果没有对应匹配文件，就删除
            os.remove(os.path.join(path2,file2))

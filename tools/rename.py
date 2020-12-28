import os
Dir = r"C:\Users\ddd\Desktop\JPEGImages"
count1=1
fileList = os.listdir(Dir)
os.chdir(Dir)
for filename in fileList:
    os.rename(filename, str(count1).zfill(3)+'.'+filename.split('.')[-1])
    count1+=1
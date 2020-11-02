import os
import zipfile

zipfile.ZipFile("flag.zip").extractall(".")
num = 1000

while True:
    try:
        lr = open("direction.txt").read()
        os.remove("direction.txt")
        #print(lr)
        zipfile.ZipFile("{}{}.zip".format(num, lr)).extractall(".")
        os.remove("{}right.zip".format(num))
        os.remove("{}left.zip".format(num))
        num-=1
    except:
        print(num)
        break
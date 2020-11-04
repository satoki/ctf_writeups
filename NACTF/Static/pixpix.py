import os
import cv2
import numpy

flag = cv2.imread("flag_bw.png")
size = len(flag) * len(flag[0])

os.makedirs("data", exist_ok=True)

for i in range(size):
    if (size % (i+1)) == 0:
        cv2.imwrite("data/flag_{}_{}.png".format(i+1, int((size / (i+1)))), numpy.reshape(flag, [int(i+1), int(size / (i+1)), -1]))
import cv2
import numpy

flag = cv2.imread("flag.png")

for i in range(len(flag)):
    for j in range(len(flag[0])):
        if not (flag[i][j] == numpy.array([0, 0, 0])).all():
            flag[i][j] = numpy.array([0, 0, 255])

cv2.imwrite("flag_bw.png", flag)
import numpy as np
from PIL import Image

image_array = np.asarray(Image.open("./NITKC.png")).copy()

with open('./flag.txt') as f:
    flag = f.read().encode()

written = 0;

for x in range(len(image_array)):
    for y in range(len(image_array[0])):
        if len(flag) > written:
            c = flag[written]
            print(c)
            red = c & 0b11
            green = (c & 0b1100) >> 2
            blue = (c &0b1110000) >> 4

            image_array[x][y][0] &= ~0b11
            image_array[x][y][0] |= red
            
            image_array[x][y][1] &= ~0b11
            image_array[x][y][1] |= green

            image_array[x][y][2] &= ~0b111
            image_array[x][y][2] |= blue
            
            print(image_array[x][y])
            written += 1

Image.fromarray(image_array).save('output.png')

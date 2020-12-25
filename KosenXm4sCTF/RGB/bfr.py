import numpy as np
from PIL import Image

image_array = np.asarray(Image.open("output.png")).copy()

text = b"abcdefghijklmnopqrstuvwxyz0123456789_!{} "

for x in range(len(image_array)):
    for y in range(len(image_array[0])):
        _flag = set()
        for r in range(256):
            for g in range(256):
                for f in text:
                    _r = r
                    _g = g
                    red = f & 0b11
                    green = (f & 0b1100) >> 2
                    _r &= ~0b11
                    _r |= red
                    _g &= ~0b11
                    _g |= green
                    if (image_array[x][y][0] == _r) and (image_array[x][y][1] == _g):
                        _flag.add(chr(f))
        print("".join(list(_flag)))
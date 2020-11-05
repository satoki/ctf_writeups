# Static:Forensics:250pts
Juliet just airdropped me this really weird photo that looks like tv static. She said this would be easier than passing notes in class, but I can't understand what she's trying to say. I think Juliet said that the message text was black. Help!  
Hint  
There seems to be some suspicious black lines in the image…  
Hint  
The final output should be an image with the flag in black text (not an encoded string, morse code, etc...)  
[flag.png](flag.png)  

# Solution
flag.pngが渡されるが、ノイズ画像のようだ。  
黒色の文字が隠れているらしいので、以下のblack.pyで黒色以外を赤色に変換する。  
```python:black.py
import cv2
import numpy

flag = cv2.imread("flag.png")

for i in range(len(flag)):
    for j in range(len(flag[0])):
        if not (flag[i][j] == numpy.array([0, 0, 0])).all():
            flag[i][j] = numpy.array([0, 0, 255])

cv2.imwrite("flag_bw.png", flag)
```
出力画像は以下になる。  
![flag_bw.png](flag_bw.png)  
所々に黒い線が入っている。  
おそらく文字が書かれていた画像(二次元配列)の縦横が変更されている。  
元の画像の縦横がわからないため以下のpixpix.pyで総当たりする。  
dataフォルダの中に変形した画像一覧が保存される。  
```python:pixpix.py
import os
import cv2
import numpy

flag = cv2.imread("flag_bw.png")
size = len(flag) * len(flag[0])

os.makedirs("data", exist_ok=True)

for i in range(size):
    if (size % (i+1)) == 0:
        cv2.imwrite("data/flag_{}_{}.png".format(i+1, int((size / (i+1)))), numpy.reshape(flag, [int(i+1), int(size / (i+1)), -1]))
```
実行後、dataフォルダ内の画像を見ていくと、以下の画像が目にとまる。  
flag_30_1100.png  
![flag_30_1100.png](data/flag_30_1100.png)  
flagが描かれていた。  

## nactf{p1x3l5}
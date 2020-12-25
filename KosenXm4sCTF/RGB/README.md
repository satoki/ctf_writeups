# RGB:Reversing:101pts
あなたは国のサイバー犯罪対策課長代理補佐だ。ある犯罪者グループが秘密のメッセージを画像中に残したという。生成された画像ファイルとその生成スクリプトを入手した。昇進のため、まずはそのメッセージを復元してほしい。  
[create_secret_image.py](create_secret_image.py)　　　　[output.png](output.png)  

# Solution
生成スクリプトは以下のようになっていた。  
```python:create_secret_image.py
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
```
画像の色にflag.txtの内容を埋め込んでいる。  
可逆な演算かもしれないが、調査が面倒なので赤色と青色のみに注目し、当てはまるものを総当たりする。  
以下のbfr.pyで行う。  
```python:bfr.py
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
```
実行する。  
```bash
$ python bfr.py
8xh
m}
4td
3sc
k{
4td
8xh
i9y
3sc
_o
i9y
3sc
_o
3sc
4td
ue5
w7g
1aq!
n
_o
w7g
b2r
1aq!
p0
8xh
i9y
1aq!
fv6
l
1aq!
w7g
_o
i9y
n
_o
i9y
m}
1aq!
w7g
ue5
1aq!
1aq!
m}
zj
n
n
3sc
^C
```
意味のある単語になるように、文字を拾っていくとflagが得られた。  

## xm4s{this_is_steganography!flag_in_image!!}
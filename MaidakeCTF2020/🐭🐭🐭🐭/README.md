# 🐭🐭🐭🐭:Misc:200pts
ねずみといえば...  
Hint  
🐭→ねずみ→マウス  
...マウス？...Pressed...Released....  
[flag.csv](flag.csv)  

# Solution
csvファイルが渡される。  
中身は以下のような形式だった。  
```csv
~~~
76,282
76,283
76,283,Pressed
76,281
76,278
~~~
154,295
153,297
153,297,Released
153,295
153,293
~~~
```
これがマウスの履歴であることはすぐにわかる。  
PressedからReleasedまでをプロットしてやればよい。  
以下のdoraemon.pyでプロットする。  
```python:doraemon.py
import matplotlib.pyplot as plt

s = open("flag.csv").readlines()
plot = 0

for i in s:
    if ",Pressed" in i:
        plot = 1
        i = i.replace(",Pressed","")
    if ",Released" in i:
        plot = 0
        i = i.replace(",Released","")
    i = i.replace("\n","")
    if plot == 1:
        x_y = i.split(",")
        plt.scatter(int(x_y[0]), -1*int(x_y[1]), color="#ff4500")
plt.show()
```
![flag.png](images/flag.png)  
flagが表示された。  

## MaidakeCTF{I_tried_to_include_a_lot_of_useless_information}
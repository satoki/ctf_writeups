# In a pickle:misc:200pts
We managed to intercept communication between und3rm4t3r and his hacker friends. However it is obfuscated using something. We just can't figure out what it is. Maybe you can help us find the flag?  
[data](data)  

# Solution
一見すると意味不明なファイルだが、pythonにはオブジェクトを保存できるpickleがあるらしい。  
dataを読み込んでprintしてみる。  
```bash
$ python
>>> import pickle
>>> print(pickle.load(open('data', mode='rb')))
{1: 'D', 2: 'UCTF', 3: '{', 4: 112, 5: 49, 6: 99, 7: 107, 8: 108, 9: 51, 10: 95, 11: 121, 12: 48, 13: 117, 14: 82, 15: 95, 16: 109, 17: 51, 18: 53, 19: 53, 20: 52, 21: 103, 22: 51, 23: '}', 24: "I know that the intelligence agency's are onto me so now i'm using ways to evade them: I am just glad that you know how to use pickle. Anyway the flag is "}
```
ASCIIコードになっている。  
以下のrottenp.pyで読み込んで表示する。  
```python:rottenp.py
import pickle
import string

text = pickle.load(open('data', mode='rb'))

print(text)
print("-"*40)

for i in range(1,24):
    try:
        print(chr(text[i]),end="")
    except:
        print(text[i],end="")
```
```bash
$ ls
data  rottenp.py
$ python rottenp.py
{1: 'D', 2: 'UCTF', 3: '{', 4: 112, 5: 49, 6: 99, 7: 107, 8: 108, 9: 51, 10: 95, 11: 121, 12: 48, 13: 117, 14: 82, 15: 95, 16: 109, 17: 51, 18: 53, 19: 53, 20: 52, 21: 103, 22: 51, 23: '}', 24: "I know that the intelligence agency's are onto me so now i'm using ways to evade them: I am just glad that you know how to use pickle. Anyway the flag is "}
----------------------------------------
DUCTF{p1ckl3_y0uR_m3554g3}
```
flagが隠れていた。

## DUCTF{p1ckl3_y0uR_m3554g3}
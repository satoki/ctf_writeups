# Unimod:Cryptography:50pts
I was trying to implement ROT-13, but got carried away.  

**Attachments:** [out](out)　[unimod.py](unimod.py)  

# Solution
スクリプトと出力ファイルが渡される。  
おそらくflagを暗号化したものだろう。  
スクリプトは以下のようであった。  
```python
import random

flag = open('flag.txt', 'r').read()
ct = ''
k = random.randrange(0,0xFFFD)
for c in flag:
    ct += chr((ord(c) + k) % 0xFFFD)

open('out', 'w').write(ct)
```
flagを読み取り、各文字に0xFFFDまでの乱数kを足して0xFFFDで割った余りが出力されている。  
ここで0xFFFDまでの乱数はASCIIより十分大きいため、`ord(c) + k`が0xFFFDを超えることはほとんどない。  
つまり`chr((ord(c) + k) % 0xFFFD)`は`chr((ord(c) + k))`とみなせる。  
あとはフラグの先頭がfから始まることを利用してkを求めて復号すればよい。  
以下のdec.pyで行う。  
```python
out = open("out", "r").read()
k = ord(out[0]) - ord("f")
flag = ""

for c in out:
    flag += chr(ord(c) - k)

print(flag)
```
実行する。  
```bash
$ python dec.py
flag{4e68d16a61bc2ea72d5f971344e84f11}

```
flagが得られた。  

## flag{4e68d16a61bc2ea72d5f971344e84f11}
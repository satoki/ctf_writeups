# do_you_like_CBC?:Crypto:152pts
メリークリスマス！これを読んでるあなたに、暗号化ソースコードのクリスマスプレゼント！  
[enc.py](enc.py)　　　　[encrypted_flag.txt](encrypted_flag.txt)  

# Solution
暗号化プログラムとその結果が渡される。  
encrypted_flag.txtは以下のようだ。  
```text:encrypted_flag.txt
flag lenght: 30
block size: 5
encrypted(your flag): b'aW4kYHpQUDt+dUVuC0tSamoWX0RjexFBT307HzwI'
```
enc.pyの以下に注目する。  
```python
~~~
key = "paswd"
blocksize = len(key)
initial_vector = "abcde"
~~~
```
keyとivがわかっているので、先頭から五文字ずつ決定できる。  
以下のdec.pyで行う。  
```python:dec.py
import math
import base64

text = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_} !?#\n"

flag = "xm4s{"

key = "paswd"
blocksize = len(key)
initial_vector = "abcde"

b = 1

while True:
    if (b == 1) and (not "}" in flag):
        b = 0
    else:
        print(flag.encode())
        break
    for i1 in text:
        if b == 1:
            break
        print(i1)
        for i2 in text:
            if b == 1:
                break
            for i3 in text:
                if b == 1:
                    break
                for i4 in text:
                    if b == 1:
                        break
                    for i5 in text:
                        _flag = flag
                        _flag += "{}{}{}{}{}".format(i1, i2, i3, i4, i5)
                        if len(_flag)%blocksize != 0:
                            _flag += '#' * (blocksize - len(_flag)%blocksize)
                        encrypted_flag = ""
                        last_enc = initial_vector
                        for i in range(0,len(_flag),blocksize):
                            asciicode = [ord(j) for j in _flag[i:i+blocksize]]
                            chain = [asciicode[j] ^ ord(last_enc[j]) for j in range(blocksize)]
                            enc = [chain[j] ^ ord(key[j]) for j in range(blocksize)]
                            enc = ''.join([chr(j) for j in enc])
                            encrypted_flag += enc
                            last_enc = enc
                        if encrypted_flag.encode("utf-8") in base64.b64decode("aW4kYHpQUDt+dUVuC0tSamoWX0RjexFBT307HzwI"):
                            print(_flag)
                            flag = _flag
                            b = 1
                            break
                        #print(encrypted_flag.encode("utf-8"))
                        #print(base64.b64decode("aW4kYHpQUDt+dUVuC0tSamoWX0RjexFBT307HzwI"))
```
実行する。  
時間がかかるため、textを適宜最適な順に並び替えてやるとよい。  
```bash
$ python dec.py
a
b
c
~~~
m
n
xm4s{I_like_CBC_encryption!}
#
b'xm4s{I_like_CBC_encryption!}\n#'
```
flagが得られた。  

## xm4s{I_like_CBC_encryption!}
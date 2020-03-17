# Shifter:Misc:160pts
What a strange challenge...  
It'll be no problem for you, of course!  
nc misc.2020.chall.actf.co 20300  
Hint  
Do you really need to calculate all those numbers?  

# Solution
nc misc.2020.chall.actf.co 20300をたたくと以下のように表示された。  
```text
Solve 50 of these epic problems in a row to prove you are a master crypto man like Aplet123!
You'll be given a number n and also a plaintext p.
Caesar shift `p` with the nth Fibonacci number.
n < 50, p is completely uppercase and alphabetic, len(p) < 50
You have 60 seconds!
--------------------
Shift SJPEYWPYHKUYXQSQQJFXNIAEXQOXQVDVO by n=37
:
```
つまりフィボナッチ数列n項目の数だけ文字列をシフトさせればよい。  
フィボナッチ数列は一般項で表せることが知られている。  
以下のプログラムにより自動化するとflagが出てくる。  
```python:shifter.py
import re
import socket
import numpy as np

def fib(n):
    f = (((1 + np.sqrt(5)) / 2)**n - ((1 - np.sqrt(5)) / 2)**n ) / np.sqrt(5)
    return int(f)

def rot(d, s):
    s = s % 26
    r = []
    for c in d:
        c = ord(c)
        c = c + s
        if c > 90:
            c = c - 26
        r.append(chr(c))
    r = "".join(r)
    return r

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("misc.2020.chall.actf.co", 20300))

while True:
    rtext = str(s.recv(512))
    if "actf" in rtext:
        print(rtext)
        break
    #print(rtext)
    se = re.search(".*Shift\s(?P<t>.*)\sby\sn=(?P<n>[0-9]*).*", rtext)
    text = se.group("t")
    #print(text)
    num = int(se.group("n"))
    #print(num)
    ans = rot(text, fib(num))
    #print(ans)
    s.sendall((ans+"\n").encode("utf-8"))
```
## actf{h0p3_y0u_us3d_th3_f0rmu14-1985098}
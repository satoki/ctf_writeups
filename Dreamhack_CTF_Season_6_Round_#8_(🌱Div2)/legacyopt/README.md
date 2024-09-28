# legacyopt:reversing:290pts
Good ol' days of optimization...  
Flag format: `DH{.*}`  

[Download challenge](beaf1d66-42d2-4ef8-b94e-1f64cf556c48.zip)  

# Solution
実行ファイルlegacyoptと暗号化されたであろうフラグのHexがoutput.txtとして配布される。  
おそらくlegacyoptをリバースし、暗号化アルゴリズムを解析して、output.txtを復号する問題だと思われる。  
面倒なのでいろいろと試していると、入力した文字数と暗号文の文字数(Hexなので2倍)が同じであることに気づく。  
```bash
$ ./legacyopt
A
72
$ ./legacyopt
AB
6371
```
output.txtが78文字なので、Hexの2倍を考慮しフラグが39文字であるとわかる。  
さらに39文字で試していると、先頭が正しいフラグのフォーマット`DH{`である文字列を暗号化すると、output.txtの先頭と一致した。  
```bash
$ cat output.txt
220c6a33204455fb390074013c4156d704316528205156d70b217c14255b6ce10837651234464e
$ ./legacyopt
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
27055036146372c927055036146372c927055036146372c927055036146372c927055036146372
$ ./legacyopt
DAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
22055036146372c927055036146372c927055036146372c927055036146372c927055036146372
$ ./legacyopt
DHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
220c5036146372c927055036146372c927055036146372c927055036146372c927055036146372
```
1文字ずつ特定することができそうだ。  
以下のsolver.pyで行う。  
```py
import string
from ptrlib import *

FLAG_LENGTH = 39
logger.level = 0

flag = ["A"] * FLAG_LENGTH
with open("output.txt", "r") as f:
    encdata = f.read()

for i in range(FLAG_LENGTH):
    for j in string.printable:
        flag[i] = j
        sock = Process("./legacyopt")
        sock.sendline("".join(flag))
        result = sock.recv(FLAG_LENGTH * 2).decode()
        if result[: (i + 1) * 2] == encdata[: (i + 1) * 2]:
            print(f"Hit: flag[{i}] = {j}")
            break
        sock.close()

print(f"flag = {''.join(flag)}")
```
実行する。  
```bash
$ python solver.py
Hit: flag[0] = D
Hit: flag[1] = H
Hit: flag[2] = {
Hit: flag[3] = D
Hit: flag[4] = u
Hit: flag[5] = f
Hit: flag[6] = f
Hit: flag[7] = s
Hit: flag[8] = _
Hit: flag[9] = D
Hit: flag[10] = e
Hit: flag[11] = v
Hit: flag[12] = i
Hit: flag[13] = c
Hit: flag[14] = e
Hit: flag[15] = _
Hit: flag[16] = b
Hit: flag[17] = u
Hit: flag[18] = t
Hit: flag[19] = _
Hit: flag[20] = u
Hit: flag[21] = s
Hit: flag[22] = e
Hit: flag[23] = _
Hit: flag[24] = m
Hit: flag[25] = e
Hit: flag[26] = m
Hit: flag[27] = c
Hit: flag[28] = p
Hit: flag[29] = y
Hit: flag[30] = _
Hit: flag[31] = i
Hit: flag[32] = n
Hit: flag[33] = s
Hit: flag[34] = t
Hit: flag[35] = e
Hit: flag[36] = a
Hit: flag[37] = d
Hit: flag[38] = }
flag = DH{Duffs_Device_but_use_memcpy_instead}
```
flagが得られた。  

## DH{Duffs_Device_but_use_memcpy_instead}
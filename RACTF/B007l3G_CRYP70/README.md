# B007l3G CRYP70:Cryptography:350pts
Challenge instance ready at 95.216.233.106:16118.  
While doing a pentest of a company called MEGACORP's network, you find these numbers laying around on an FTP server:   
41 36 37 27 35 38 55 30 40 47 35 34 43 35 29 32 38 37 33 45 39 30 36 27 32 35 36 52 72 54 39 42 30 30 58 27 37 44 72 47 28 46 45 41 48 39 27 27 53 64 32 58 43 23 37 44 32 37 28 50 37 19 51 53 30 41 18 45 79 46 40 42 32 32 46 28 37 30 43 31 26 56 37 41 61 68 44 34 26 24 48 38 50 37 27 31 30 38 34 58 54 39 30 33 38 18 33 52 34 36 31 33 28 36 34 45 55 60 37 48 57 55 35 60 22 36 38 34. Through further analysis of the network, you also find a network service running. Can you piece this information together to find the flag?  

# Solution
ncすると以下のように表示される。  
```bash
Welcome to MEGACORP's proprietary encryption service! Just type your message below and out will come the encrypted text!

Please enter the message you wish to encrypt: a
Your encrypted message is: 38 53 25 42

Please enter the message you wish to encrypt: a
Your encrypted message is: 38 40 28 52

Please enter the message you wish to encrypt: a
Your encrypted message is: 33 40 38 47

Please enter the message you wish to encrypt: a
Your encrypted message is: 40 44 43 31

Please enter the message you wish to encrypt: a
Your encrypted message is: 31 22 55 50

Please enter the message you wish to encrypt: b
Your encrypted message is: 37 31 55 34

Please enter the message you wish to encrypt: b
Your encrypted message is: 37 34 52 34

Please enter the message you wish to encrypt: b
Your encrypted message is: 38 34 35 50

Please enter the message you wish to encrypt:
~~~
```
暗号化されており、鍵も毎回変わっているように見える。  
38+53+25+42=158  
38+40+28+52=158  
暗号ではなく、ただの和分解のようだ。  
まずは`abcdefghijklmnopqrstuvwxyz0123456789{}_`の数値を取得する。  
```bash
$ nc 95.216.233.106 16118
Welcome to MEGACORP's proprietary encryption service! Just type your message below and out will come the encrypted text!

Please enter the message you wish to encrypt: abcdefghijklmnopqrstuvwxyz0123456789{}_
Your encrypted message is: 24 51 51 32 36 26 43 52 37 38 55 26 37 49 27 42 36 30 56 32 42 45 45 21 55 38 27 32 50 26 35 40 43 29 40 38 43 33 51 22 28 37 36 47 38 49 41 19 49 28 47 22 27 31 32 55 51 27 31 35 29 51 38 25 41 41 18 42 19 36 43 43 28 36 29 47 24 32 29 54 35 29 52 22 14 41 37 45 30 44 40 22 43 25 36 31 28 41 30 35 42 38 38 15 32 57 48 70 34 49 69 54 19 63 62 61 57 32 62 53 35 62 60 46 34 68 38 62 38 61 60 42 64 25 46 65 71 33 39 56 55 58 28 57 37 23 49 23 45 41 28 16 41 33 49 37
```
四桁ずつ足し込んでいけば文字に対応する数値がわかる。
以下のwadec.pyでデコードする。  
```python:wadec.py
import numpy as np

text = "abcdefghijklmnopqrstuvwxyz0123456789{}_"
gettext = [24,51,51,32,36,26,43,52,37,38,55,26,37,49,27,42,36,30,56,32,42,45,45,21,55,38,27,32,50,26,35,40,43,29,40,38,43,33,51,22,28,37,36,47,38,49,41,19,49,28,47,22,27,31,32,55,51,27,31,35,29,51,38,25,41,41,18,42,19,36,43,43,28,36,29,47,24,32,29,54,35,29,52,22,14,41,37,45,30,44,40,22,43,25,36,31,28,41,30,35,42,38,38,15,32,57,48,70,34,49,69,54,19,63,62,61,57,32,62,53,35,62,60,46,34,68,38,62,38,61,60,42,64,25,46,65,71,33,39,56,55,58,28,57,37,23,49,23,45,41,28,16,41,33,49,37]

c = [41,36,37,27,35,38,55,30,40,47,35,34,43,35,29,32,38,37,33,45,39,30,36,27,32,35,36,52,72,54,39,42,30,30,58,27,37,44,72,47,28,46,45,41,48,39,27,27,53,64,32,58,43,23,37,44,32,37,28,50,37,19,51,53,30,41,18,45,79,46,40,42,32,32,46,28,37,30,43,31,26,56,37,41,61,68,44,34,26,24,48,38,50,37,27,31,30,38,34,58,54,39,30,33,38,18,33,52,34,36,31,33,28,36,34,45,55,60,37,48,57,55,35,60,22,36,38,34]

t = list(np.array_split(gettext, int(len(gettext)/4)))
t = list(map(lambda x: sum(x), t))
c = list(np.array_split(c, int(len(c)/4)))
c =list(map(lambda x: sum(x), c))

for i in range(len(c)):
    for j in range(len(t)):
        if c[i] == t[j]:
            print(text[j], end="")
print()
```
実行するとflagが出てくる。  
```bash
$ python wadec.py
ractf{d0n7_r0ll_y0ur_0wn_cryp70}
```

## ractf{d0n7_r0ll_y0ur_0wn_cryp70}
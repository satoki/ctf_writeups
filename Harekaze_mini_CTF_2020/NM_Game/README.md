# NM Game:Misc:179pts
天才的なAIを開発しました。少し戦ってみましょう。  
nc 20.48.84.64 20001  

---

We built a genius AI. Let's play a game.  
nc 20.48.84.64 20001  

---

# Solution
ncで接続してみる。  
```bash
$ nc 20.48.84.64 20001
Be the last to take a pebble!
Creating a new problem...
15
How many pebbles do you want to take? [1-3]: 3
The opponent took 2 from 0
10
How many pebbles do you want to take? [1-3]: 2
The opponent took 1 from 0
7
How many pebbles do you want to take? [1-3]: 3
The opponent took 2 from 0
2
How many pebbles do you want to take? [1-2]: 2
Won!
Remaining games: 14
Creating a new problem...
25 28
Choose a heap [0-1]: ^C
```
NIMのAIのようだ。  
このまま問題数が増加していくことは目に見えているので、自動化する。  
基本戦略としては、すべてのheapを4で割った余りのxorが0となるような手を相手に押しつければよい。  
以下のnimnim.pyで行う。  
```python:nimnim.py
import pwn
import sys
import copy
from functools import reduce

def win(nums):
    num = [i % 4 for i in nums]
    num = reduce(lambda a, b: a ^ b, num, 0)
    return not num

io = pwn.remote("20.48.84.64", 20001)
fmsg = io.recvline()
#print(fmsg)

while True:
    while True:
        msg = io.recvline()
        #print(msg)
        if b"HarekazeCTF{" in msg:
            print(msg)
            sys.exit(0)
        try:
            now = [int(i) for i in (io.recvline().decode()).split(" ")]
            print(now)
        except:
            break
        bflag = 0
        for i in range(len(now)):
            if bflag == 1:
                break
            for j in range(1,4):
                _now = copy.copy(now)
                _now[i] -= j
                if win(_now):
                    if _now[i] < 0:
                        continue
                    io.sendline(str(i))
                    io.sendline(str(j))
                    #print(i, j)
                    bflag = 1
                    break
```
実行する。  
```bash
$ python nimnim.py
[+] Opening connection to 20.48.84.64 on port 20001: Done
[23]
[17]
[13]
[9]
[5]
[1]
[17, 11]
~~~
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3]
b'Congratulations! Here is the flag: HarekazeCTF{pe6b1y_qRundY_peb6l35}\n'
```
flagが表示された。  

## HarekazeCTF{pe6b1y_qRundY_peb6l35}
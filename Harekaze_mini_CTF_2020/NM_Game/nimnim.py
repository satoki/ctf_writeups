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
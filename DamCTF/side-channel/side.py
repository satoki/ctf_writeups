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
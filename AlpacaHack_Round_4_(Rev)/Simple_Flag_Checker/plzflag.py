import re
import string
from ptrlib import *

logger.level = 0

flag = ["x"] * 49

for i in range(49):
    for c in string.printable:
        sock = Process("gdb ./checker")
        sock.sendlineafter("pwndbg> ", "start")
        sock.sendlineafter("pwndbg> ", "b *0x0000555555555a2a")
        sock.sendlineafter("pwndbg> ", "c")
        flag[i] = c
        sock.sendline("".join(flag))
        for j in range(i):
            sock.sendlineafter("pwndbg> ", "c")
        sock.recvuntil("s1")
        result = sock.recvuntil("pwndbg> ").decode()
        sock.close()
        result = re.sub(r"\x1b\[[0-9;]*m", "", result)
        s1_s2 = re.findall(r"◂—\s*(0x[0-9a-fA-F]+)", result)
        if s1_s2[0] == s1_s2[1]:
            print(f"flag[{i}] = {c}")
            break

print(f"flag = {''.join(flag)}")

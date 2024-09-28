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

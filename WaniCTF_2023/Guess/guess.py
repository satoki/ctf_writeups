import collections
from pwn import *

context.log_level = "error"

ANSWER = ["-1"] * 10**4

p = remote("guess-mis.wanictf.org", 50018)

index = 0
while index < 10**4:
    p.recvuntil(b"> ")
    p.sendline(b"1")
    p.recvuntil(b"index> ")
    payload = []
    for i in range(index, index + 1000):
        for _ in range((i % 1000) + 1):
            payload.append(f"{i}")
    payload = " ".join(payload)
    # print(payload) #Debug
    p.sendline(payload.encode())
    resp = collections.Counter(eval(p.recvline().decode())).most_common()
    for i in range(index, index + 1000):
        ANSWER[i] = f"{resp[-((i % 1000) + 1)][0]}"
    # print(ANSWER) #Debug
    index += 1000
    print(f"{index}/{10**4}")

p.recvuntil(b"> ")
p.sendline(b"2")
p.recvuntil(b"Guess the list> ")
p.sendline((" ".join(ANSWER)).encode())

p.interactive()

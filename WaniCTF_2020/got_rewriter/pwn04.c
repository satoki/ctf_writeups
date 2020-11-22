#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

void init();

void win()
{
    puts("congratulation!");
    system("/bin/sh");
    exit(0);
}

void vuln()
{
    char str_val[0x20];
    unsigned long int val;
    unsigned long int *p;
    int ret;

    printf("Please input target address (0x600e10-0x6010b0): ");
    ret = read(0, str_val, 0x20);
    str_val[ret - 1] = 0;
    val = strtol(str_val, NULL, 16);
    printf("Your input address is 0x%lx.\n", val);
    if (val < 0x600e10 || val > 0x6010b0)
    {
        printf("you can't rewrite 0x%lx!\n", val);
        return;
    }
    p = (unsigned long int *)val;

    printf("Please input rewrite value: ");
    ret = read(0, str_val, 0x20);
    str_val[ret - 1] = 0;
    val = strtol(str_val, NULL, 16);
    printf("Your input rewrite value is 0x%lx.\n\n", val);

    printf("*0x%lx <- 0x%lx.\n\n\n", (unsigned long int)p, val);
    *p = val;
}

int main()
{
    init();
    puts("Welcome to GOT rewriter!!!");
    printf("win = 0x%lx\n", (unsigned long int)win);
    while (1)
    {
        vuln();
    }
}

void init()
{
    alarm(30);
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

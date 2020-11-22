#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

void init();
void debug_stack_dump(unsigned long rsp, unsigned long rbp);

char str_head[] = "hello ";
char str_tail[] = "!\n";

void win()
{
    puts("Congratulation!");
    system("/bin/sh");
    exit(0);
}

void vuln()
{
    char target[] = "HACKASE";
    char name[10];
    char *p;
    int ret;

    printf("What's your name?: ");
    ret = read(0, name, 0x100);
    name[ret - 1] = 0;

    write(0, str_head, strlen(str_head));
    write(0, name, strlen(name));
    write(0, str_tail, strlen(str_tail));

    if (strncmp(target, "WANI", 4) == 0)
    {
        win();
    }
    else
    {
        printf("target = %s\n", target);
    }

    { //for learning stack
        register unsigned long rsp asm("rsp");
        register unsigned long rbp asm("rbp");
        debug_stack_dump(rsp, rbp);
    }
}

int main()
{
    init();
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

void debug_stack_dump(unsigned long rsp, unsigned long rbp)
{
    unsigned long i;
    printf("\n***start stack dump***\n");
    i = rsp;
    while (i <= rbp + 8)
    {
        unsigned long *p;
        p = (unsigned long *)i;
        printf("0x%lx: 0x%016lx", i, *p);
        if (i == rsp)
        {
            printf(" <- rsp");
        }
        else if (i == rbp)
        {
            printf(" <- rbp");
        }
        else if (i == rbp + 8)
        {
            printf(" <- return address");
        }
        printf("\n");
        i += 8;
    }
    printf("***end stack dump***\n\n");
}

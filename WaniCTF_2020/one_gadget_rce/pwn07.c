#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

char str_head[] = "hello ";
char str_tail[] = "!\n";

void init();
void debug_stack_dump(unsigned long rsp, unsigned long rbp);

void vuln()
{
    char name[10];
    int ret;

    printf("What's your name?: ");
    ret = read(0, name, 0x100);
    name[ret - 1] = 0;

    write(0, str_head, strlen(str_head));
    write(0, name, strlen(name));
    write(0, str_tail, strlen(str_tail));

    { //for learning stack
        register unsigned long rsp asm("rsp");
        register unsigned long rbp asm("rbp");
        debug_stack_dump(rsp, rbp);
    }
}

int main()
{
    init();
    puts("Welcome to one-gadget RCE!!!");
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
    puts("\n***start stack dump***");
    i = rsp;
    while (i <= rbp + 32)
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
    puts("***end stack dump***\n");
}

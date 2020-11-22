#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

char str_head[] = "Please input \"";
char binsh[] = "/bin/sh";
char str_tail[] = "\" address as a hex number: ";

void init();

void vuln()
{
    char name[0x20];
    unsigned long int val;
    char *p;
    int ret;

    write(0, str_head, strlen(str_head));
    write(0, binsh, strlen(binsh));
    write(0, str_tail, strlen(str_tail));

    ret = read(0, name, 0x20);
    name[ret - 1] = 0;
    val = strtol(name, NULL, 16);
    printf("Your input address is 0x%lx.\n", val);
    p = (char *) val;
    if(p == binsh){
        puts("Congratulation!");
        system(p);
        exit(0);
    }else{
        puts("You are wrong.\n\n");
    }
}

int main()
{
    init();
    printf("The address of \"input  \" is 0x%lx.\n", (unsigned long int) str_head);    
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

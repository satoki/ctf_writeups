#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

void init();

void win()
{
    puts("congratulation!");
    system("/bin/sh");
    exit(0);
}

int main()
{
    init();
    win();
}

void init()
{
    alarm(30);
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

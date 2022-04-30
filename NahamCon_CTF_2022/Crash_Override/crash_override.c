#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <signal.h>

void win(int sig) {
    FILE *fp = NULL;
    char *flag = NULL;
    struct stat sbuf;

    if ((fp = fopen("flag.txt", "r")) == NULL) {
        puts("Failed to open the flag. If this is on the challenge server, contact an admin.");
        exit(EXIT_FAILURE);
    }

    if (fstat(fileno(fp), &sbuf)) {
        puts("Failed to get flag.txt file status. If this is on the challenge server, contact an admin.");
        exit(EXIT_FAILURE);
    }

    flag = calloc(sbuf.st_size + 1, sizeof(char));
    if (!flag) {
        puts("Failed to allocate memory.");
        exit(EXIT_FAILURE);
    }

    fread(flag, sizeof(char), sbuf.st_size, fp);
    puts(flag);

    free(flag);

    exit(EXIT_SUCCESS);
}

int main(void) {
    char buffer[2048];

    setbuf(stdin, NULL);
    setbuf(stdout, NULL);

    signal(SIGSEGV, win);

    puts("HACK THE PLANET!!!!!!");
    gets(buffer);

    return 0;
}

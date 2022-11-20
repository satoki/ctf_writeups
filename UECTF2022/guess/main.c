#include <stdio.h>
#include <string.h>

void win() {
    char flag[0x20];
    FILE *fp = fopen("flag.txt", "r");
    fgets(flag, 32, fp);
    puts(flag);
    fclose(fp);
}

void secret(char *s) {
    FILE *fp = fopen("secret.txt", "r");
    fgets(s, 32, fp);
    fclose(fp);
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    char buf[32];
    char pw[32];

    secret(pw);

    printf("Guess my password\n> ");
    scanf("%32s", buf);
    if(strncmp(pw, buf, sizeof(pw)) == 0) {
        puts("Correct!!!");
        win();
    } else {
        puts("Wrong.");
    }
    return 0;
}

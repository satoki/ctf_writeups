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


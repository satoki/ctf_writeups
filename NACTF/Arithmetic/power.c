#include <stdio.h>
#include <stdint.h>

int main() {
    int64_t a = 0;
    while ((uint32_t) a + (uint32_t) 2718281828 != 42) {
        a++;
    }
    printf("%ld\n",a);
    return 0;
}
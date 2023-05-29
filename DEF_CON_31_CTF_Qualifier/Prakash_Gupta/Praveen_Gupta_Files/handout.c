#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include "seccomp-bpf.h"


// Your base64_decode() function goes here


int jail()
{
	// [REDACTED]
}


int main()
{
    jail();

    char buffer[1024];
    scanf("%1023s", buffer);
    char* data = base64_decode(buffer);
    if (data != NULL) {
        printf("%s\n", data);
        free(data);
    }
}

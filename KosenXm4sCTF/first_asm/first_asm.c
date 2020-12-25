/*
gcc -O0 -o binary binary.c check_flag.s
*/

#include <stdio.h>
#include <stdbool.h>

extern bool check_flag(char* input);

int main(void) {
	char input[33];
	printf("+------------+\n");
	printf("|FLAG CHECKER|\n");
	printf("+------------+\n");
	printf("Input: ");
	scanf("%32s%*c", input);
	if (check_flag(input)) {
		printf("Correct!\n");
	} else {
		printf("Wrong...\n");
	}
}

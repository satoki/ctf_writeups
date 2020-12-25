#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>

void call_me_to_win() {
	system("/bin/sh");
}

int main() {
	// set up for CTF
  setvbuf(stdin, NULL, _IONBF, 0); 
  setvbuf(stdout, NULL, _IONBF, 0);
	alarm(60);

	
	printf("call_me_to_win at %p\n", call_me_to_win);

	unsigned long value = 1; // I like unsigned long value!
	printf("%lx\n", &value);

	size_t where, what;

	printf("where:");
	scanf("%lx", &where);
	printf("what:");
	scanf("%lx", &what);

	*(size_t*)where = what; // where に what を書き込む
}




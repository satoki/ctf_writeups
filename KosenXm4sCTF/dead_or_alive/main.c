#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>

char* get_secret_password() {
	char password[0x1000]; // I can get very very long password!!
	
	FILE *fp = fopen("./password.txt", "r");
	if(fp == NULL) {
		puts("password.txt not found.");
		exit(0);
	}
	fgets(password, 0x1000, fp);
	char* ret = password;

	return ret;
}

void login(char *password) {
	char input[512];
	printf("Input your password:");
	fgets(input, 512, stdin);

	if(strcmp(input, password) == 0) {
		puts("You logged in!");
		system("/bin/sh");
	}
}

void hello() {
	char name[0x1000];
	
	puts("Tell me your name!");
	fgets(name, 0x1000, stdin);

	printf("Hello %s\n", name);
}

int menu() {
	int ret;

	printf(
			"0: Hello\n"
			"1: Login\n"
			);

	scanf("%d%*c", &ret);

	return ret;
}

int main() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  alarm(60);
	
	char* pass = get_secret_password();
	while(1) {
		int option = menu();
		if(option == 0) {
			hello();
		} else if(option == 1) {
			login(pass);
		}
	}
}




#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>

int main() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  alarm(60);

  char program[0x1000];

  puts("Enter your program!");
  fgets(program, 0x1000, stdin);

  FILE *fp = fopen("/tmp/program.c", "w");
  fprintf(fp, "%s", program);
  fclose(fp);

  system("rm /tmp/program");
  system("gcc /tmp/program.c -o /tmp/program");
  system("/tmp/program");
  system("rm /tmp/program");
}

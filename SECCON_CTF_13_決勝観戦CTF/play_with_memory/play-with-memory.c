#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

void print_flag() {
  char flag[256];
  int fd = open("./flag.txt", O_RDONLY);
  if (fd < 0) { puts("./flag.txt not found"); return; }
  write(1, flag, read(fd, flag, sizeof(flag)));
}

int main() {
  setbuf(stdout, NULL);
  
  int number = 0;
  printf("input your number!: ");
  scanf("%4s", &number);

  if (number == 12345) {
    print_flag();
  } else {
    printf("number: %d (0x%x)", number, number);
  }
  return 0;
}

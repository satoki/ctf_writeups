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

void bye() {
  puts("bye!");
}

int main() {
  setbuf(stdout, NULL);

  char buf[8];
  void (*funcptr)() = bye;
  
  printf("address of print_flag func: %p\n", print_flag);
  printf("gets to buf: ");
  gets(buf);
  printf("content of funcptr: %p\n", funcptr);
  funcptr();
  return 0;
}

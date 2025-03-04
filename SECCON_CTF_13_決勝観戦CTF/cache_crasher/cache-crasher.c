#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

#define MAX_ALLOC 0x10

union chunk {
  union chunk* next_chunk;
  size_t val;
};

size_t alloced = 0;
union chunk buf[MAX_ALLOC];
union chunk* cache = NULL;
union chunk* allocate() {
  size_t a = sizeof(union chunk);

  union chunk* res;
  if (cache != NULL) {
    res = cache;
    cache = res->next_chunk;
  }
  else {
    if (MAX_ALLOC <= alloced) return NULL; // buf exhausted
    res = &buf[alloced];
    alloced++;
  }

  return res;
}

void free_chunk(union chunk* ptr) {
  ptr->next_chunk = cache;
  cache = ptr;
}

void print_flag() {
  char flag[256];
  int fd = open("./flag.txt", O_RDONLY);
  if (fd < 0) { puts("./flag.txt not found"); return; }
  write(1, flag, read(fd, flag, sizeof(flag)));
}

void dump_info() { // You don't need to read this function!
  printf("Cache:\n");
  union chunk* current = cache; int limit = 5;
  while (buf <= current && current < &buf[MAX_ALLOC]) {
    printf("%p -> ", (void*)current);
    current = current->next_chunk;
    if (--limit == 0) { printf("...\n"); break; }
  }
  if (limit != 0) printf("%p\n", (void*)current);
  printf("Buffer:\n");
  for (size_t i = 0; i < alloced; i++) printf("buf[%zu]: %p (val: 0x%lx)\n", i, (void*)&buf[i], buf[i].val);
}

void (*funcptr)() = dump_info;

#define ALLOC 0
#define FREE  1
int main() {
  setbuf(stdout, NULL);
  printf("address of print_flag: %p\n", print_flag);
  printf("address of funcptr: %p\n", &funcptr);

  int i = 0;
  union chunk* s[MAX_ALLOC];

  int opcode;
  while (1) {
    printf("opcode(0: alloc, 1: free): ");
    if (scanf("%d", &opcode) == EOF) break;
    if (opcode == ALLOC) {
      size_t val;
      s[i] = allocate();
      if (s[i] == NULL) { perror("allocate failed"); exit(1); } 
      printf("data(integer): ");
      if (scanf("%zu", &val) == EOF) break;
      s[i]->val = val;
      i++;
    }
    else {
      size_t ind;
      printf("what index to free: ");
      if (scanf("%zu", &ind) == EOF) break;
      if (ind < 0 || i <= ind) { perror("invalid operand"); exit(1); }
      free_chunk(s[ind]);
    }

    printf("content of funcptr: %p\n", funcptr);
    funcptr();
  }
}

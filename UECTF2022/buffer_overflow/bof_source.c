#include<stdio.h>
#include<string.h>
int debug();
int main(){
  char debug_flag,name[15];
  debug_flag='0';
  printf("What is your name?\n>");
  scanf("%s",name);
  if(debug_flag=='1'){
    debug();
  }
  printf("Hello %s.\n",name);
  return 0;
}

int debug(){
  char flag[32]="CTF{THIS_IS_NOT_TRUE_FLAG}";
  printf("[DEBUG]:flag is %s\n",flag);
}

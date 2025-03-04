# Can U Keep A Secret?:Pwn:100pts
Or ...?  
```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

int main() {
    srand(time(NULL));
    unsigned int secret = rand(), input;
    printf("secret: %u\n", secret);

    // can u keep a secret??/
    secret *= rand();
    secret *= 0x5EC12E7;
    scanf("%u", &input);
    if(input == secret)
        printf("Alpaca{REDACTED}\n");
    return 0;
}
```
_*完全なソースコードは以下からダウンロード可能です。_  

[can-u-keep-a-secret.tar.gz](can-u-keep-a-secret.tar.gz)  

`nc 34.170.146.252 59556`  

# Solution
Cソースと接続先が渡される。  
`srand(time(NULL))`を行い、`= rand()`、`*= rand()`、`*= 0x5EC12E7`の順で作成した`secret`を当てればいいようだ。  
一度目の`rand()`後の`secret`は表示される。  
加工した実行ファイルをローカルで実行し続け、一度目の`secret`が一致するものの最終的な`secret`を入力するようにすれば、サーバの時間がある程度ずれていても関係ない。  
以下のように加工する。  
```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

int main() {
    srand(time(NULL));
    unsigned int secret = rand(), input;
    printf("secret: %u\n", secret);

    // can u keep a secret??/
    secret *= rand();
    secret *= 0x5EC12E7;
    printf("input: %u\n", secret); // :)
    scanf("%u", &input);
    if(input == secret)
        printf("Alpaca{REDACTED}\n");
    return 0;
}
```
コンパイルすると警告が表示された。  
```bash
$ gcc a.c
a.c: In function ‘main’:
a.c:11:27: warning: trigraph ??/ ignored, use -trigraphs to enable [-Wtrigraphs]
   11 |     // can u keep a secret??/
      |
```
トライグラフというC言語の機能が使われているらしい。  
これによるとコメント末尾だと思っていた`??/`が実際には`\`となり、一行下の`secret *= rand();`までもが複数行のコメントとみなされるようだ。  
そのため、実際には`secret`には`= rand()`、`*= 0x5EC12E7`しか行われていない。  
ただの掛け算なので以下のように解く。  
```bash
$ nc 34.170.146.252 59556
secret: 1092663764
108564247055210060
Alpaca{u_r_pwn_h3r0}
```
flagが得られた。  

## Alpaca{u_r_pwn_h3r0}
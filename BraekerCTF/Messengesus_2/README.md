# Messengesus 2:Crypto / Hashcracking:100pts
The bot quickly turns away to scribble new lines in the holy code. He turns back, "Uh, well.. he..hear the word of RNGesus again! Praised be the secured code. No need to repeat what you've seen here."  
Can you praise this secured code?  
![messengesus2.jpeg](messengesus2.jpeg)  

[messengesus2.zip](messengesus2.zip)  

# Solution
[Messengesus](../Messengesus)の続き？のようだ。  
以下のようなソースと暗号化されたファイルciphertextが与えられた。  
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main() {

    char secret[] = "brck{not_the_flag}";
    size_t secret_length = strlen(secret);
    char *key = NULL;
    size_t read_length, buffer_length = 0;
    
    // Read One Time Key
    FILE *random_bytes = fopen("/dev/urandom", "rb");
    if (random_bytes == NULL)
        return 0;
    read_length = getline(&key, &buffer_length, random_bytes);
    fclose(random_bytes);

    // Encrypt
    for (int i = 0; i < secret_length; i++)
        secret[i] = secret[i] ^ key[i];

    free(key);

    // Security!
    if (read_length < secret_length) {
        return 0;
    }

    // Store encrypted secret
    FILE *output_file = fopen("./ciphertext", "ab");
    if (output_file == NULL)
        return 0;
    fwrite(secret, 1, secret_length, output_file);
    fclose(output_file);

    return 0;
}
```
動作としては、フラグを変数`secret`とし、一文字ずつ`/dev/urandom`由来の乱数keyでxorしている。  
ただし、乱数がフラグの長さを下回ることはないようだ。  
つまり、[Messengesus](../Messengesus)のように`0x0a`のような文字だけでの復号はできない。  
ciphertextを確認すると、ファイルサイズが大きいため、上記プログラムを何度も実行した結果であるようだ。  
よって、複数の暗号文が得られていることになる。  
ソースを読んでいると`getline`を使っていることに気付く。  
この関数は改行で読み取りを停止するため、keyの途中に`0x0a`が含まれることは無い。  
例えば一文字目は`b`(`0x62`)であるが、暗号文の一文字目に`0x62 ^ 0x0a`である`h`(`0x68`)は出現しないこととなる。  
つまり、暗号文のN文字目に対し`0x0a`でxorした結果のアルファベットはフラグのN文字目でないことになる。  
フラグ長が不明なため、ciphertextを順に区切り、複数個となった暗号化されたフラグをから復号を試みる。  
以下のsolve2.pyで行う。  
```python
with open("ciphertext", "rb") as f:
    data = f.read()

for flag_len in range(1, len(data)):
    flag = ""
    if len(data) % flag_len:
        continue
    cflags = [data[x : x + flag_len] for x in range(0, len(data), flag_len)]
    for i in range(flag_len):
        clist = [chr(f[i] ^ 0x0A) for f in cflags]
        c = "".join(set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?_{}") - set(clist))
        flag += c
    if "brck{" in flag:
        print(f"flag_len: {flag_len}")
        print(flag)
        break
```
実行する。  
```bash
$ python solve2.py
flag_len: 34
brck{St1ll_n0th1ng_bUt_4_b4by_p4d
```
末尾の`}`は`0x0a`となる(乱数とフラグの長さが一致する)場合もあり、欠落する。  
直してやるとflagとなった。  

## brck{St1ll_n0th1ng_bUt_4_b4by_p4d}
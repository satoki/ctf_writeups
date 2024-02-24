# Messengesus:Crypto / Hashcracking:150pts
You encounter a bot meditating in the park. He opens his cameras and begins to speak.  
"Hear the word of RNGesus. Complexity is the enemy of security. Let your encryption be as simple as possible, as to secure it, thusly". He hands you a flyer with a snippet of code. "Secure every message you have with it. Only those who see can enter."  
What do you think? Is it simple enough to be secure?  
![messengesus.jpg](messengesus.jpg)  

`nc 0.cloud.chals.io 26265`  

[messengesus.c](messengesus.c)  

# Solution
接続先とソースが渡される。  
ソースは以下のようであった。  
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main() {

    char secret[] = "brck{not_the_flag}";
    char *key = NULL;
    size_t read_length, buffer_length = 0;
    
    // Read One Time Key
    FILE *random_bytes = fopen("/dev/urandom", "r");
    read_length = getline(&key, &buffer_length, random_bytes);
    fclose(random_bytes);

    // Encrypt
    for (int i = 0; i < strlen(secret); i++)
        secret[i] = secret[i] ^ key[i%read_length];

    // Return encrypted secret
    printf("%s", secret);

    free(key);
    return 0;
}
```
フラグを一文字ずつxorで暗号化しているようだ。  
keyは`/dev/urandom`から乱数を`getline`で読み取っている。  
ここで、`getline`が改行までしか読み取らないことに気付く。  
もし乱数が`0x0a`から始まっていた場合、その一文字だけをkeyとして用いることとなる。  
以下のsolve.pyで256分の1を当てればよい。  
```python
from ptrlib import *

logger.level = 0

while True:
    try:
        sock = Socket("nc 0.cloud.chals.io 26265")
        data = list(sock.recv(42))
        for i in range(len(data)):
             data[i] ^= 0x0A
        xor_data = bytes(data)
        print(xor_data)
        sock.close()
        if b"brck{" in xor_data:
            break
    except:
        pass
```
実行する。  
```bash
$ python solve.py
b'\x82\xbal9$\xff\xb2\xb8D\x8d]\x05\x90R"Q\xb0]\x06\xe0\xe4\xd0\x11\xcdqY\x0f\x8c\x9a\xdb\x9f/N\x8bUH\x04\x8d\xe7\x86\x9a\xe0'
b'-<\xba\xcc\xa0\xc5\xfb\xc9\x9d]\xd1\x7f\x16\x9f\xd5m\x9c\xb3[\xcc\x14\x1a\x12"\xf0[leI%\x11<\xdd\xc1w\x08P\x8a$\xa7v\xa9'
~~~
b'\xa3\xdd\x16&h\xc57\xe6\x8f\x89\xa7QwtiD\xc4\x12Y\\\xb5\xe0\x10\x1dmCt\x81\xbf\x8c\x9f7RW\xa6\xa9\x99m\x01\xeeC\x1a'
b'brck{SiMPl1c1Ty_1s_K3Y_But_N0t_th3_4nSW3r}'
```
flagが得られた。  

## brck{SiMPl1c1Ty_1s_K3Y_But_N0t_th3_4nSW3r}
# reverse_easy:rev:70pts
難易度：★★☆  
週末何してますか？忙しいですか？リバースエンジニアリングしてもらっていいですか？  

[reverse_easy](reverse_easy)  

# Solution
リバースエンジニアリングする必要があるらしい。  
配布ファイルを調べると入力をフラグと比較する系の問題のようだ。  
```bash
$ file reverse_easy
reverse_easy: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=e165d1d3ff8cf89e2cb248601393acc9243c4427, for GNU/Linux 3.2.0, not stripped
$ ./reverse_easy
input flag : Satoki
wrong...
```
angrゲーかと思いつつstringsしてみる。  
```bash
$ strings reverse_easy
~~~
KogCTF2023{5tr1ng5_c0mm4nd_1s_ve8y_u5efu1}
input flag :
correct!
wrong...
~~~
$ ./reverse_easy
input flag : KogCTF2023{5tr1ng5_c0mm4nd_1s_ve8y_u5efu1}
correct!
```
flagが得られた。  

## KogCTF2023{5tr1ng5_c0mm4nd_1s_ve8y_u5efu1}
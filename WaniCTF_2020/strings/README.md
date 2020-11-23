# strings:Reversing:101pts
この問題ではLinuxのELF実行ファイル(バイナリ)である「strings」が配布されています。このバイナリは入力文字列をチェックし、正しいものかどうか判定する機能をもっています。  
試しにFAKE{this_is_fake}と入力するとIncorrectと表示され、間違っている入力文字列であると示してくれます。  
このバイナリが「正しい」と判定してくれる文字列を見つけ出してください。  
ヒント：バイナリ解析のはじめの一歩は「表層解析」という手法です。  
(このファイルを実行するためにはLinux環境が必要となりますのでWSLやVirtualBoxで用意してください)  
```bash
$ file strings
strings: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=78a1aa79cb6ab262c29bc2302ac50dc5f29e4d78, not stripped

$ sudo chmod +x strings

$ ./strings
input flag : FAKE{this_is_fake}
Incorrect
```
[strings](strings)  

# Solution
神問題。  
stringsすればよい。  
```bash
$ ./strings
input flag : Satoki
Incorrect
$ strings strings | grep FLAG
FLAG{s0me_str1ngs_rem4in_1n_t7e_b1nary}
$ ./strings
input flag : FLAG{s0me_str1ngs_rem4in_1n_t7e_b1nary}
Correct! Flag is FLAG{s0me_str1ngs_rem4in_1n_t7e_b1nary}
```
flagが隠されていた。  

## FLAG{s0me_str1ngs_rem4in_1n_t7e_b1nary}
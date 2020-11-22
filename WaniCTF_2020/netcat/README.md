# netcat:PWN:pts
nc netcat.wanictf.org 9001  
- netcat (nc)と呼ばれるコマンドを使うだけです。  
- つないだら何も表示されなくても知っているコマンドを打ってみましょう。  

使用ツール例  
- [netcat (nc)](https://github.com/wani-hackase/memo-setup-pwn-utils#netcat)  

gccのセキュリティ保護  
- Full RELocation ReadOnly (RELRO)  
- Stack Smash Protection (SSP)有効  
- No eXecute bit(NX)有効  
- Position Independent Executable (PIE)有効  

[pwn01](pwn01)　　　　[pwn01.c](pwn01.c)  

# Solution
ncの練習問題。  
以下のように行う。  
```bash
$ nc netcat.wanictf.org 9001
congratulation!
ls
chall
flag.txt
redir.sh
cat flag.txt
FLAG{netcat-1s-sw1ss-4rmy-kn1fe}
^C
```
flagが得られた。  

## FLAG{netcat-1s-sw1ss-4rmy-kn1fe}
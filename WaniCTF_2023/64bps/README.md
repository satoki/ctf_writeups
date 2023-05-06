# 64bps:Web:157pts
```bash
dd if=/dev/random of=2gb.txt bs=1M count=2048
cat flag.txt >> 2gb.txt
rm flag.txt
```
↓↓↓  
[https://64bps-web.wanictf.org/2gb.txt](https://64bps-web.wanictf.org/2gb.txt)  

[web-64bps.zip](web-64bps.zip)  

# Solution
不穏なコマンド、URL、ソースらしきファイルが与えられる。  
コマンドより、1M*2048のランダムファイルの末尾にフラグを追記しているようだ。  
ソース内のnginx.confを見ると以下の通りであった。  
```conf
~~~
http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    keepalive_timeout  65;
    gzip               off;
    limit_rate         8; # 8 bytes/s = 64 bps

    server {
        listen       80;
        listen  [::]:80;
        server_name  localhost;

        location / {
            root   /usr/share/nginx/html;
            index  index.html index.htm;
        }
    }
}
```
`limit_rate`によりファイルをすべて取ってくるのは厳しい。  
ここでRangeヘッダーを思い出す。  
うまく計算してフラグの箇所のみを抜いてやればよい。  
```bash
$ echo $((1048576*2048))
2147483648
$ curl https://64bps-web.wanictf.org/2gb.txt -H "Range: bytes=2147483648-"
FLAG{m@ke_use_0f_r@n0e_reques7s_f0r_l@r9e_f1les}
```
flagが得られた。  

## FLAG{m@ke_use_0f_r@n0e_reques7s_f0r_l@r9e_f1les}
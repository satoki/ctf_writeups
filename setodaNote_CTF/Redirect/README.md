# Redirect:Web:150pts
組織の関連サイトを監視している部署から「どうやら会長ブログが何らか侵害を受けてしまっているようだ」と連絡が入りました。再現方法が不明なものの、一部の訪問者から不審なサイトに飛ばされてしまうという指摘がされているようです。上司は休暇で不在ですが特に支障はありません。被害を最小にすべくサイトを調査し侵害状況を把握してください。  
以下のサイトにアクセスしてフラグを見つけ出してください。  
[https://ctf.setodanote.net/web004/](https://ctf.setodanote.net/web004/)  

# Solution
アクセスすると謎のページが出てくる。  
Web - setodaNote CTF  
[site1.png](site/site1.png)  
サイト内におかしなところが見当たらないため、ソースを見ると以下のような記述があった。  
```html
~~~
<script>!function(){var ref = document.referrer;var domain = ref.match(/^http([s]?):\/\/([a-zA-Z0-9-_\.]+)(:[0-9]+)?/)[2];if(domain == "www.google.com" || domain == "www.google.co.jp" ){location.href = atob('aHR0cHM6Ly9jdGYuc2V0b2Rhbm90ZS5uZXQvd2ViMDA0L2JXRnNhMmwwLmh0bWw=');}}();</script>
~~~
```
`location.href = atob('aHR0cHM6Ly9jdGYuc2V0b2Rhbm90ZS5uZXQvd2ViMDA0L2JXRnNhMmwwLmh0bWw=');`が明らかに怪しい。  
base64をデコードすると`https://ctf.setodanote.net/web004/bWFsa2l0.html`なのでアクセスするが、複数回のリダイレクトを繰り返し以下のサイトへ遷移する。  
Nice try!  
[site2.png](site/site2.png)  
リダイレクト途中のサイトに何らかの情報が含まれていると考え、それぞれのアドレスを取得すると以下のようであった。  
```bash
$ curl https://ctf.setodanote.net/web004/bWFsa2l0.html
~~~
    <script>
      !function() {
        var params = new URL(window.location.href).searchParams;
        if(Array.from(params).length > 0){
          location.href = 'https://ctf.setodanote.net/web004/bm9mbGFn/?'+params;
        }else{
          location.href = 'https://ctf.setodanote.net/web004/bWFsa2l0.html?callback=wantFlag&data1=2045&data2=0907&data3=BiancoRoja&data4=1704067200';
        }
      }();
    </script>
~~~
$ curl https://ctf.setodanote.net/web004/bm9mbGFn/
~~~
        location.href = 'https://ctf.setodanote.net/web004/bmV4dG5leHQ/?'+params
~~~
$ curl https://ctf.setodanote.net/web004/bmV4dG5leHQ/
~~~
        location.href = 'https://ctf.setodanote.net/web004/b25lLXR3by10aHJlZQ/?'+params
~~~
$ curl https://ctf.setodanote.net/web004/b25lLXR3by10aHJlZQ/
<html>
  <head>
    <title>Branching point</title>
    <noscript>
      <meta http-equiv=refresh content="1; URL=https://ctf.setodanote.net/web004/noscript.html">
    </noscript>
    <script>
      !function() {
        var params = new URL(window.location.href).searchParams;
        if (params.get('callback') == 'getFlag') {
          location.href = 'https://ctf.setodanote.net/web004/dGFjaGlrb21hX2thd2FpaV95b25l/?' + params;
        }else{
          location.href = 'https://ctf.setodanote.net/web004/ZGFtbXlmbGFn/?' + params;
        }
      }();
      </script>
  </head>
  <body>
  <p>You need the correct parameters to get the flag.</p>
  </body>
</html>
```
パスがbase64されていそうだが、ダミーのようだ(tachikoma_kawaii_yoneってw)。  
途中で怪しいgetFlagなるものが出現した。  
適切なクエリを設定し、以下をブラウザで閲覧する。  
```text
https://ctf.setodanote.net/web004/dGFjaGlrb21hX2thd2FpaV95b25l/?callback=getFlag&data1=2045&data2=0907&data3=BiancoRoja&data4=1704067200
```
すると以下に遷移し、flagを得ることができた。  
```text
https://noisy-king-d0da.setodanote.net/?callback=getFlag&data1=2045&data2=0907&data3=BiancoRoja&data4=1704067200
```
flag  
[flag.png](site/flag.png)  

## flag{Analyz1ng_Bad_Red1rects}
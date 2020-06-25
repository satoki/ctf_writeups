# login:web:148pts
I made a cool login page. I bet you can't get in!  
Site: [login.2020.redpwnc.tf](https://login.2020.redpwnc.tf/)  
[index.js](index.js)  

# Solution
アクセスするとログインフォームが見える。  
Login  
[site.png](site/site.png)  
index.jsを見ると以下の記述がある。  
```JavaScript
~~~
    let result;
    try {
        result = db.prepare(`SELECT * FROM users 
            WHERE username = '${username}'
            AND password = '${password}';`).get();
    } catch (error) {
        res.json({ success: false, error: "There was a problem." });
        res.end();
        return;
    }
~~~
```
SQLインジェクションが行えそうだ。  
`t' OR 't' = 't`を入力するとflagがアラートされた。  

## flag{0bl1g4t0ry_5ql1}
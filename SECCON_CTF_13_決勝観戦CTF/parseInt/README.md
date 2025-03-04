# parseInt:Misc:100pts
`a < b && parseInt(a) > parseInt(b)` となるような `a`, `b` を見つけてください🐟  
```javascript
const rl = require("node:readline").createInterface({
    input: process.stdin,
    output: process.stdout,
});

rl.question("Input a,b: ", input => {
    const [a, b] = input.toString().trim().split(",").map(Number);
    if (a < b && parseInt(a) > parseInt(b))
        console.log(process.env.FLAG);
    else
        console.log(":(");
    rl.close();
});
```
_*完全なソースコードは以下からダウンロード可能です。_  

[parse-int.tar.gz](parse-int.tar.gz)  

`nc 34.170.146.252 47322`  

# Solution
問題文の通り`a,b`の数値入力を受け取り、`a < b && parseInt(a) > parseInt(b)`となればいいようだ。  
`parseInt`をかけて大きさが逆転するような不審な挙動があるか試す。  
```js
$ node
~~~
> 100000000000000000000
100000000000000000000
> 1000000000000000000000
1e+21
> parseInt(100000000000000000000)
100000000000000000000
> parseInt(1000000000000000000000)
1
```
このような問題では、巨大な数の挙動が直感に反することが多い。  
試しに`1000000000000000000000`を用いると`1e+21`となり、`parseInt`は数値として読み取れる箇所(eの前)までを数値に変換するため1が返ってくる。  
これで大きさの逆転を引き起こせそうだ。  
以下のように問題サーバへ投げる。  
```bash
$ nc 34.170.146.252 47322
Input a,b: 100000000000000000000,1000000000000000000000
100000000000000000000,1000000000000000000000
Alpaca{..ww.w....<')))><.~~~}
```
魚のflagが得られた。  

## Alpaca{..ww.w....<')))><.~~~}
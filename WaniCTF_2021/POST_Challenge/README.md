# POST Challenge:Web:181pts
HTTP POSTに関する問題を5つ用意しました。すべて解いてFLAGを入手してください！  
[https://post.web.wanictf.org/](https://post.web.wanictf.org/)  
[web-http-post.zip](web-http-post.zip)  

# Solution
POSTを複数回行って各チャレンジをクリアしていくサイトのようだ。  
POST Challenge  
[site.png](site/site.png)  
配布されたソースを見る。  
chal1は以下のようであった。  
```JavaScript
app.post("/chal/1", function (req, res) {
  let FLAG = null;
  if (req.body.data === "hoge") {
    FLAG = process.env.FLAG_PART1;
  }
  res.render("chal", { FLAG, chal: 1 });
});
```
`req.body.data === "hoge"`なのでdataに`hoge`を入れればよい。  
```bash
$ curl -X POST https://post.web.wanictf.org/chal/1 --data "data=hoge"
~~~
  Congratulations! Challenge 1 FLAG: y0u
~~~
```
chal2は以下のようであった。  
```JavaScript
app.post("/chal/2", function (req, res) {
  // リクエストヘッダのUser-AgentにどのブラウザでもついているMozilla/5.0がある場合のみFLAGを送信
  let FLAG = null;
  if (
    req.headers["user-agent"].includes("Mozilla/5.0") &&
    req.body.data === "hoge"
  ) {
    FLAG = process.env.FLAG_PART2;
  }
  res.render("chal", { FLAG, chal: 2 });
});
```
UAを`Mozilla/5.0`にすればよい。  
```bash
$ curl -X POST https://post.web.wanictf.org/chal/2 --data "data=hoge" -H "User-Agent: Mozilla/5.0"
~~~
  Congratulations! Challenge 2 FLAG: ar3
~~~
```
chal3は以下のようであった。  
```JavaScript
app.post("/chal/3", function (req, res) {
  let FLAG = null;
  if (req.body.data?.hoge === "fuga") {
    FLAG = process.env.FLAG_PART3;
  }
  res.render("chal", { FLAG, chal: 3 });
});
```
data[hoge]に`fuga`を入れればよい。  
```bash
$ curl -X POST https://post.web.wanictf.org/chal/3 --data "data[hoge]=fuga"
~~~
  Congratulations! Challenge 3 FLAG: http
~~~
```
chal4は以下のようであった。  
```JavaScript
app.post("/chal/4", function (req, res) {
  let FLAG = null;
  if (req.body.hoge === 1 && req.body.fuga === null) {
    FLAG = process.env.FLAG_PART4;
  }
  res.render("chal", { FLAG, chal: 4 });
});
```
hogeが`1`でfugaが`null`である必要がある。  
`Content-Type: application/json`でPOSTしてやる。  
```bash
$ curl -X POST https://post.web.wanictf.org/chal/4 --data '{"hoge":1,"fuga":null}' -H "Content-Type: application/json"
~~~
  Congratulations! Challenge 4 FLAG: p0st
~~~
```
chal5は以下のようであった。  
```JavaScript
function md5file(filePath) {
  const target = fs.readFileSync(filePath);
  const md5hash = crypto.createHash("md5");
  md5hash.update(target);
  return md5hash.digest("hex");
}

app.post("/chal/5", function (req, res) {
  let FLAG = null;
  if (req.files?.data?.md5 === md5file("public/images/wani.png")) {
    FLAG = process.env.FLAG_PART5;
  }
  res.render("chal", { FLAG, chal: 5 });
});
```
md5が一致するもの、つまりwani.pngを送れと言っている。  
トップページのワニをPOSTすればよい。  
```bash
$ wget https://post.web.wanictf.org/images/wani.png
~~~
$ curl -X POST https://post.web.wanictf.org/chal/5 -F data=@wani.png -H "Content-Type: multipart/form-data"
~~~
  Congratulations! Challenge 5 FLAG: m@ster!
~~~
```
これらchal1~5を指定されたとおりに整形するとflagとなった。  

## FLAG{y0u_ar3_http_p0st_m@ster!}
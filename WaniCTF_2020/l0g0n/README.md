# l0g0n:Crypto:pts
🕵️‍♂️  
nc l0g0n.wanictf.org 50002  
[server.py](server.py)  

# Solution
server.pyが配布される。  
これがサーバ側で動いているようだ。  
Crypto問だが暗号は解けそうにないので筋力を使う。  
mainに注目する。  
```python
~~~
def main():
    while True:
        client_challenge = input("Challenge (hex) > ")
        client_challenge = bytes.fromhex(client_challenge)

        server_challenge = os.urandom(8)
        print(f"Server challenge: {server_challenge.hex()}")

        session_key = key_derivation_function(psk + client_challenge + server_challenge)

        client_credential = input("Credential (hex) > ")
        client_credential = bytes.fromhex(client_credential)

        cipher = AES_CFB8(session_key)
        server_credential = cipher.encrypt(client_challenge)
        if client_credential == server_credential:
            print(f"OK! {flag}")
        else:
            print("Authentication Failed... 🥺")
~~~
```
入力が空である場合にifの条件が真となってしまう。  
以下のようにハックする。  
```bash
$ nc l0g0n.wanictf.org 50002
Challenge (hex) >
Server challenge: fb159aadf182f6f2
Credential (hex) >
OK! b'FLAG{4_b@d_IV_leads_t0_CVSS_10.0__z3r01090n}'
Challenge (hex) >
Server challenge: 2b745555ca975bcf
Credential (hex) >
OK! b'FLAG{4_b@d_IV_leads_t0_CVSS_10.0__z3r01090n}'
Challenge (hex) >
Server challenge: 6f04762c94b7f3c6
Credential (hex) >
OK! b'FLAG{4_b@d_IV_leads_t0_CVSS_10.0__z3r01090n}'
Challenge (hex) >
Server challenge: 98fb47bac05cf6a1
Credential (hex) >
OK! b'FLAG{4_b@d_IV_leads_t0_CVSS_10.0__z3r01090n}'
Challenge (hex) >
Server challenge: 2b663cfd007aabfc
Credential (hex) >
OK! b'FLAG{4_b@d_IV_leads_t0_CVSS_10.0__z3r01090n}'
Challenge (hex) > ^C
```
flagが得られた。  

## FLAG{4_b@d_IV_leads_t0_CVSS_10.0__z3r01090n}
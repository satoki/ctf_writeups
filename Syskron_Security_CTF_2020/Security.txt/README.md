# Security.txt:Tuesday:200pts
The security.txt draft got updated ([https://tools.ietf.org/html/draft-foudil-securitytxt-10](https://tools.ietf.org/html/draft-foudil-securitytxt-10)).  
Is Senork's file still up-to-date? [https://www.senork.de/.well-known/security.txt](https://www.senork.de/.well-known/security.txt)  
Unlock Hint for 20 points  
Signed files offer more security but less privacy.  

# Solution
PGP SIGNATUREがあるようだ。  
OpenPGP keyを保存し、以下のコマンドを実行するとflagが得られる。  
```bash
$ wget https://www.senork.de/openpgp.asc
~~~
$ gpg openpgp.asc
gpg: *警告*: コマンドが指定されていません。なにを意味しているのか当ててみます ...
pub   ed25519 2020-09-04 [SC] [有効期限: 2020-11-03]
      1BD03A9A7ABD58DD6E0DC68C29714015001FE8C2
uid           BB Industry a.s. PSIRT (syskronCTF{Wh0-put3-flag3-1nto-0penPGP-key3???}) <psirt@bb-industry.cz>
```

## syskronCTF{Wh0-put3-flag3-1nto-0penPGP-key3???}
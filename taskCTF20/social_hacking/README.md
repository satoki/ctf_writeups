# social hacking:Misc:10pts
[https://www.youtube.com/watch?v=t1zPpBwRbAw](https://www.youtube.com/watch?v=t1zPpBwRbAw)  
checksum(sha256): 8b47b48f802573fb016f60926310b80bda5dd66e76fad30c0cf11b656762fff8  
[secret.zip](secret.zip)  

# Solution
secret.zipが配られるが、パスワードがかかっている。  
問題文のURLから動画([guess \`?v=\`](../guess_`%3Fv=`)と同じもの)を見ると、後半にパスワードをつぶやいているような箇所がある。  
聞き取りにくいが`onigiri`+誕生日と言っている。  
作問者の誕生日は`1205`なのでパスワードは`onigiri1205`とわかる。  
zipを解凍する。  
```bash
$ unzip secret.zip
Archive:  secret.zip
   creating: secret/
[secret.zip] secret/flag.txt password:
 extracting: secret/flag.txt
$ cat secret/flag.txt
taskctf{n0t1ce_soci4l_h4ck1ng}
```
flagが得られた。  

## taskctf{n0t1ce_soci4l_h4ck1ng}
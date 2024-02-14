# google form:Survey:0pts
アンケートにご協力ください  
よろしくお願いいたします  
[https://forms.gle/tpMuGkZxeBqtMj639](https://forms.gle/tpMuGkZxeBqtMj639)  

# Solution
アンケートに答えるとフラグが手に入るようだ。  
問題名がgoogle formなのでフォームから盗み出せとの意図を感じる。  
```bash
$ curl -sL https://forms.gle/tpMuGkZxeBqtMj639 | grep -o 'shioCTF{.*}'
shioCTF{Thank_you_very_much!}
```
flagが得られた(もちろんアンケートにも答えた)。  

## shioCTF{Thank_you_very_much!}
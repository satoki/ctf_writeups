# rot-i:crypto:100pts
ROT13 is boring!  
Attached files:  
- challenge.txt (sha256: ab443133665f34333aa712ab881b6d99b4b01bdbc8bb77d06ba032f8b1b6d62d)  

[challenge.txt](challenge.txt)  

# Solution
ROT13では解けないようだ。  
challenge.txtの先頭を見ると、どうやらYouから始まっていそうである。  
```text:challenge.txt
Ypw'zj zwufpp hwu txadjkcq dtbtyu kqkwxrbvu! Mbz cjzg kv IAJBO{ndldie_al_aqk_jjrnsxee}. Xzi utj gnn olkd qgq ftk ykaqe uei mbz ocrt qi ynlu, etrm mff'n wij bf wlny mjcj :).
```
YがY、oがp、uがw。  
つまりrot-iのiが1ずつズレていっている。  
`IAJBO{ndldie_al_aqk_jjrnsxee}`を復元したいため、IがDになるrot21から始めればよい(rot-(26-i)になる)。  
[rot13.com](https://rot13.com/)を使ってもよい。  
大文字小文字の違いによる実装が面倒なので、{の後のn、つまりrot15から中身を復元するのが効率的である。  
以下のrotrotrot.pyで復元する。  
```python:rotrotrot.py
rotflag = "ndldie_al_aqk_jjrnsxee"

print("DUCTF{",end="")

i = 15
for j in rotflag:
        m = (ord(j) - ord('a') + i) % 26
        ans = chr(m + ord('a'))
        if j == "_":
            ans = j
        print(ans,end="")
        i -= 1

print("}")
```
```bash
$ python rotrotrot.py
DUCTF{crypto_is_fun_kjqlptzy}
```

## DUCTF{crypto_is_fun_kjqlptzy}
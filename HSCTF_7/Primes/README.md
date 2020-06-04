# Primes:Miscellaneous:100pts
Primes!  
[Primes.txt](Primes.txt)  

# Solution
Primes.txtを見ると、意味不明な文字列が記されている。  
しかし、一文字目がf、二文字あけてl、三文字あけてa、五文字あけてgと続いている。  
素数文字のノイズが入っていると考えてよいだろう。  
pskip.pyで抽出する。  
```python:pskip.py
from sympy import sieve

p = 1#BOM
MAXP = 100000
s = open("Primes.txt").read()
for i in sieve.primerange(2,MAXP):
    print(s[p],end="")
    if s[p] == "}":
        print()
        break
    p += i + 1
```
```bash
$ python pskip.py
flag{h1din9_1n_pl41n_519ht}
```
抽出したものがflagだった。  

## flag{h1din9_1n_pl41n_519ht}
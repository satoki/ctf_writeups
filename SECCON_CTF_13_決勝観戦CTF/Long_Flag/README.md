# Long Flag:Crypto:100pts
出力からフラグを復元してください🐍  
```python
import os
from Crypto.Util.number import bytes_to_long

print(bytes_to_long(os.getenv("FLAG").encode()))
```
出力:  
```
35774448546064092714087589436978998345509619953776036875880600864948129648958547184607421789929097085
```

# Solution
`bytes_to_long`されているので、逆の`long_to_bytes`を行えばよい。  
以下の通り行う。  
```bash
$ python
~~~
>>> from Crypto.Util.number import long_to_bytes
>>> long_to_bytes(35774448546064092714087589436978998345509619953776036875880600864948129648958547184607421789929097085)
b'Alpaca{LO00OO000O00OOOO0O00OOO00O000OOONG}'
```
flagが得られた。  

## Alpaca{LO00OO000O00OOOO0O00OOO00O000OOONG}
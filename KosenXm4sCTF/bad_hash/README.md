# bad_hash:Crypto:97pts
二人でいれば衝突なんて怖くないっ！  
```
nc 27.133.155.191 30010
```
[hash.py](hash.py)  

# Solution
オレオレハッシュ関数が動いている。  
```bash
$ nc 27.133.155.191 30010
ans_x 88, ans_m 36
test
inp_x 22, inp_m 48
```
ソースを読むと、入力のハッシュ値をパスワードのハッシュ値と衝突させれば良いようだ。  
hash.pyの以下に注目する。  
```python:hash.py
~~~
def hash(base):
    xor_sum = 0
    mod_sum = 0
    for c in base.encode():
        xor_sum ^= c
        mod_sum += c
        mod_sum %= 100
   
    return (xor_sum, mod_sum)
~~~
```
XORの累積が88となり、和を累積し100で割った余りが36となればよい。  
88は文字"X"であり、XORは同じものをかけると元に戻る性質がある。  
以下のようにXORを変化させず、和を調節する。  
```bash
$ python
~~~
>>> def hash(base):
...     xor_sum = 0
...     mod_sum = 0
...     for c in base.encode():
...         xor_sum ^= c
...         mod_sum += c
...         mod_sum %= 100
...
...     return (xor_sum, mod_sum)
...
>>> hash("X")
(88, 88)
>>> hash("XAA")
(88, 18)
>>> hash("XBB")
(88, 20)
>>> hash("XCC")
(88, 22)
>>> hash("XJJ")
(88, 36)
```
`XJJ`がパスワードと衝突する。  
```bash
$ nc 27.133.155.191 30010
ans_x 88, ans_m 36
XJJ
inp_x 88, inp_m 36
You hava a password!!
xm4s{xor_and_modsum!double_hash!!}
```
flagが得られた。  

## xm4s{xor_and_modsum!double_hash!!}
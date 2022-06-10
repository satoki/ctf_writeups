# eunectes-murinus:reversing:450pts
The green anaconda (Eunectes murinus), also known as the giant anaconda, common anaconda, common water boa or sucuri, is a boa species found in South America. It is the heaviest and one of the longest known extant snake species. Like all boas, it is a non-venomous constrictor.  
Downloads  
[eunectes-murinus.pyc](eunectes-murinus.pyc)  

# Solution
pycファイルが配布される。  
これをデコンパイルしてフラグを探せばよいようだ。  
`uncompyle6`で以下のように試みる。  
```bash
$ uncompyle6 eunectes-murinus.pyc
# uncompyle6 version 3.8.0
# Python bytecode 3.9.0 (3425)
# Decompiled from: Python 3.8.10 (default, Mar 15 2022, 12:22:08)
# [GCC 9.4.0]
# Embedded file name: chall.py
# Compiled at: 2022-05-27 13:33:01
# Size of source mod 2**32: 14269 bytes

Unsupported Python version, 3.9.0, for decompilation


# Unsupported bytecode in file eunectes-murinus.pyc
# Unsupported Python version, 3.9.0, for decompilation
```
3.9.0には対応していないようだ。  
対応しているものを「pyc 3.9.0 decompile」などで探すと、[pycdc](https://github.com/zrax/pycdc)なるものが見つかる。  
以下のように利用する。  
```bash
$ git clone https://github.com/zrax/pycdc.git
~~~
$ cd pycdc/
$ cmake CMakeLists.txt
~~~
$ sudo make
~~~
$ cd ..
$ ./pycdc/pycdc eunectes-murinus.pyc > eunectes-murinus.py
```
以下のようにデコンパイルされた。  
```python
# Source Generated with Decompyle++
# File: eunectes-murinus.pyc (Python 3.9)


def fun():
    (x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, x19, x20, x21, x22, x23, x24, x25, x26, x27, x28, x29, x30, x31, x32, x33, x34, x35, x36, x37, x38, x39, x40, x41, x42, x43, x44, x45, x46, x47, x48, x49, x50, x51, x52, x53, x54, x55, x56, x57) = input('flag?\n').encode()
    (covellite = x9, x24, halloysite = x24)
    if akimotoite * 8 * (covellite - 4) * (halloysite + 4) != 9711352:
        return print('Failed')
    (allanite = x13, x35, akimotoite = x35)
    if chalcocite * 7 * (allanite - 3) * (akimotoite + 3) != 3764768:
        return print('Failed')
    (kurnakovite = x45, x19, chalcocite = x19)
    if akimotoite * 2 * (kurnakovite - 8) * (chalcocite + 1) != 1248000:
        return print('Failed')
    (covellite = x35, x11, chalcocite = x11)
    if fayalite * 7 * (covellite - 2) * (chalcocite + 5) != 7452648:
        return print('Failed')
    (covellite = x27, x3, akimotoite = x3)
    if fayalite * 1 * (covellite - 7) * (akimotoite + 7) != 1013650:
        return print('Failed')
~~~
    (covellite = x32, x18, akimotoite = x18)
    if pyrophanite * 8 * (covellite - 3) * (akimotoite + 4) != 9270480:
        return print('Failed')
    return x32('Success')

fun()
```
謎の比較で難読化されている。  
x0~x57までがフラグの文字に対応しており、それをいくつかの整数と足し引きしているようだ。  
```python
~~~
    (covellite = x9, x24, halloysite = x24)
    if akimotoite * 8 * (covellite - 4) * (halloysite + 4) != 9711352:
        return print('Failed')
~~~
```
上記に注目すると次の計算が成立するものがフラグとなると読める。  
```
謎の変数 * 8 * (フラグの10文字目 - 4) * (フラグの25文字目 + 4) == 9711352
```
謎の変数がよくわからないため、総当たりを考える。  
以下のようなbf.pyで行う。  
```python
bullets = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_"

for b1 in bullets:
    for b2 in bullets:
        for b3 in bullets:
            i = ord(b1)
            j = ord(b2)
            k = ord(b3)
            if i * 8 * (j - 4) * (k + 4) == 9711352:
                print(b1, b2, b3)
```
実行する。  
```bash
$ python bf.py
e i s
e { a
w i a
```
フラグの途中に`{`はありえないので、x9は`i`でx24は`s or a`であることがわかる。  
より正しいものにするため、以下の部分に注目する。  
```python
~~~
    (covellite = x27, x3, akimotoite = x3)
    if fayalite * 1 * (covellite - 7) * (akimotoite + 7) != 1013650:
        return print('Failed')
~~~
```
ここではフラグの4文字目が計算に使用されている。  
このようにx0~x4、x57を起点に各文字を導けばよい。  
複数の可能性が出現した場合は、他の場所との関連性から導出できる。  
手動でスクリプトの実行を数十回行い、各文字の関連性を整理すると以下のような情報が得られる。  
```
#x0:f
#x1:l
#x2:a
#x3:g
#x4:{
#x5:i
#x6:m
#x7:a
#x8:g
#x9:i
#x10:n
#x11:e
#x12:f or _
#x13:s
#x14:o
#x15:l
#x16:v
#x17:i
#x18:n
#x19:g
#x20:_
#x21:t
#x22:h
#x23:i
#x24:s
#x25:_
#x26:c
#x27:h
#x28:a
#x29:a or l
#x30:l
#x31:e or 1 or _
#x32:n
#x33:f or g
#x34:e
#x35:_
#x36:m
#x37:a
#x38:n
#x39:o or u
#x40:a
#x41:l or n
#x42:l
#x43:y
#x44:_
#x45:8
#x46:b
#x47:6
#x48:2
#x49:f or r or 6
#x50:e
#x51:3
#x52:1
#x53:b
#x54:1
#x55:c
#x56:b
#x57:}
```
x49のように、これ以上可能性を絞ることができないものもある。  
おおよその単語が見つけられるので、形を整えると以下のようになる。  
```
flag{imagine_solving_this_challenge_manually_8b62(f/r/6)e31b1cb}
```
3パターンを試すと`6`がflagであった。  
手動でやったよ……泣

## flag{imagine_solving_this_challenge_manually_8b626e31b1cb}
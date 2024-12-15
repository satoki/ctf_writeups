# simple calc:misc:156pts
Made my first calculator—with a special bonus! 🌟  

`nc 34.146.186.1 53117`  

[simple_calc.tar.gz](simple_calc.tar.gz)  

# Solution
接続先が渡される。  
接続するとシンプルな計算機のようだ。  
```bash
$ nc 34.146.186.1 53117
1+6
7 th character is *

$ nc 34.146.186.1 53117
7*7
49 th character is *

```
計算結果の後にわけのわからない出力があるので、配布されたserver.pyを見る。  
```py
from unicodedata import numeric

text = '*' * 12345678 + "FAKECTF{THIS_IS_FAKE}" + '*' * 12345678

# I made a simple calculator :)
def calc(s):
    if (loc := s.find('+')) != -1:
        return calc(s[:loc]) + calc(s[loc+1:])
    if (loc := s.find('*')) != -1:
        return calc(s[:loc]) * calc(s[loc+1:])
    x = 0
    for c in s: x = 10 * x + numeric(c)
    return x

def check(s):
    if not all(c.isnumeric() or c in '+*' for c in s):
        return False
    if len(s) >= 6: # I don't like long expressions!
        return False
    return True

s = input()
if check(s):
    val = int(calc(s))
    print(f'{val} th character is {text[val]}')
else:
    print(':(')
```
計算は`+`と`*`が実装されており、`calc`では再帰的に値を10倍し`numeric(c)`を足すという雑な実装である。  
条件として5桁までの入力が許可されている。  
もちろん`c.isnumeric()`のように数値であるかもチェックされている。  
わけのわからない出力は、`text = '*' * 12345678 + "FAKECTF{THIS_IS_FAKE}" + '*' * 12345678`から計算結果後の文字を出力しているようだ。  
つまり、5桁までの計算式で12345678~の結果を作れということらしい。  
普通に考えると不可能だが、`numeric`は以下のように各種Unicode文字を数値と解釈することが知られている。  
```bash
$ python
~~~
>>> from unicodedata import numeric
>>> numeric("１")
1.0
>>> numeric("⑳")
20.0
>>> numeric("兆")
1000000000000.0
```
1文字で複数桁を作ることができるため、これら挙動を使えとのことらしい。  
面倒なので総当たりする方針をとる。  
5桁の文字列の総当たりは難しいが、4桁なら十分可能そうだ。  
4桁でどのような数値を作ればいいかと考えると、`1234567`を作成すればよい(5桁目を`8`とすれば`12345678`、`⑳`とすれば`12345690`(`1234567 * 10 + 20`)となる)。  
以下のbf.pyで`1234567`付近になるものを総当たりする。  
```py
import itertools
from unicodedata import numeric


# server.py
def calc(s):
    if (loc := s.find("+")) != -1:
        return calc(s[:loc]) + calc(s[loc + 1 :])
    if (loc := s.find("*")) != -1:
        return calc(s[:loc]) * calc(s[loc + 1 :])
    x = 0
    for c in s:
        x = 10 * x + numeric(c)
    return x


chars = {}
for i in range(0xFFFFF):
    try:
        c = chr(i)
        if (c).isnumeric():
            if numeric(c) not in chars:
                chars[int(numeric(c))] = c
    except:
        pass

chars = list(chars.values())
chars.append("+")
chars.append("*")

permutations = ["".join(p) for p in itertools.permutations(chars, 4)]
for p in permutations:
    if abs(1234567 - calc(p)) < 5:
        print(f"FOUND: raw: {p}")
        print(f"<num: {calc(p)}, diff: {1234567 - calc(p)}>")
```
実行する。  
```bash
$ python bf.py
FOUND: raw: 𞴽㉔𐄲𒐳
<num: 1234566.6666666667, diff: 0.3333333332557231>
FOUND: raw: ༬𐄩༰𒐳
<num: 1234565.0, diff: 2.0>
FOUND: raw: 𐄠㉑㊼𒐳
<num: 1234570.0, diff: -3.0>
FOUND: raw: 𐄠㉒㊲𒐳
<num: 1234570.0, diff: -3.0>
FOUND: raw: 𐄠㉓㉗𒐳
<num: 1234570.0, diff: -3.0>
FOUND: raw: 𐄠㉔ᛮ𒐳
<num: 1234570.0, diff: -3.0>
FOUND: raw: 𐄠㉕༰𒐳
<num: 1234565.0, diff: 2.0>
```
`1234567`は無いが、`1234565`や`1234566.6`は作成できる。  
`1234565`には`㉘`、`1234566.6`には`⑫`を続けることで`12345678`となった。  
```bash
$ nc 34.146.186.1 53117
༬𐄩༰𒐳㉘
12345678 th character is T

$ nc 34.146.186.1 53117
𞴽㉔𐄲𒐳⑫
12345678 th character is T

```
丸数字は㊿まであるため、それをすべて利用すればよい。  
以下のsolve.pyで行う。  
```py
from ptrlib import *

logger.level = 0

num = [
    "⑫",
    "⑬",
    "⑭",
    "⑮",
    "⑯",
    "⑰",
    "⑱",
    "⑲",
    "⑳",
    "㉑",
    "㉒",
    "㉓",
    "㉔",
    "㉕",
    "㉖",
    "㉗",
    "㉘",
    "㉙",
    "㉚",
    "㉛",
    "㉜",
    "㉝",
    "㉞",
    "㉟",
    "㊱",
    "㊲",
    "㊳",
    "㊴",
    "㊵",
    "㊶",
    "㊷",
    "㊸",
    "㊹",
    "㊺",
    "㊻",
    "㊼",
    "㊽",
    "㊾",
    "㊿",
]

for i in num:
    sock = Socket("nc 34.146.186.1 53117")
    sock.sendline(f"𞴽㉔𐄲𒐳{i}")
    print(sock.recvline().decode()[-1], end="")
    sock.close()
```
実行する。  
```bash
$ python solve.py
TSGCTF{Num63r5_b0w_+o_y0ur_bri11i4nC3!}
```
flagが得られた。  

## TSGCTF{Num63r5_b0w_+o_y0ur_bri11i4nC3!}
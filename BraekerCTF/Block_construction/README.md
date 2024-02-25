# Block construction:Crypto / Hashcracking:150pts
"Sir, sir! This is a construction site." You look up at what you thought was a building being constructed, but you realize it is a construction bot. "Sir please move aside. I had to have these blocks in order since last week, but some newbie construction bot shuffled them." "I can move aside, " you tell the bot, "but I might be able to help you out."  
Can you help the bot get the blocks in order?  
![block_construction.jpeg](block_construction.jpeg)  

[block_construction.zip](block_construction.zip)  

# Solution
ソースが渡される。  
中にはスクリプトと、暗号化された結果のciphertextが含まれていた。  
ソースは以下の通りであった。  
```python
import binascii 
from Crypto.Cipher import AES
from os import urandom
from string import printable
import random
from time import time


flag = "brck{not_a_flag}"
key = urandom(32)

def encrypt(raw):
	cipher = AES.new(key, AES.MODE_ECB)
	return binascii.hexlify(cipher.encrypt(raw.encode()))

# Generate random bytes
random.seed(int(time()))
rand_printable = [x for x in printable]
random.shuffle(rand_printable)

# Generate ciphertext
with open('ciphertext','w') as fout:
	for x in flag:
		for y in rand_printable:
			# add random padding to block and encrypt
			fout.write(encrypt(x + (y*31)).decode())
```
フラグの各文字を順に取り出し、31文字のパディングを加え`AES.MODE_ECB`で暗号化したhexをファイルに書き込んでいる。  
パディングは印字可能な文字をシャッフルした`rand_printable`のすべての文字で行うよう実装されている。  
つまり、フラグ一文字に対し100通り(`len(rand_printable) = 100`)のパディングを行っている。  
例えば`rand_printable = ["s", "a", "t", ...]`の順である場合、平文は以下のようになる。  
```
bsssssssssssssssssssssssssssssss
baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
bttttttttttttttttttttttttttttttt
~~~
rsssssssssssssssssssssssssssssss
raaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
rttttttttttttttttttttttttttttttt
~~~
csssssssssssssssssssssssssssssss
caaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
cttttttttttttttttttttttttttttttt
~~~
```
keyは`urandom(32)`で予測不能であり、`rand_printable`もランダムにシャッフルされている。  
復号するにあたってまず初めに`random.seed(int(time()))`といういかにも特定してくれという実装について考える。  
`time()`は暗号化結果のファイルciphertextの更新日時から分かりそうだ。  
すると`rand_printable`のシャッフル後がわかるので、パディングの文字列の順番がわかる。  
ここでECBは同じ鍵を用いて同じ平文ブロックを暗号化すると、同じ暗号文ブロックになったことを思い出す。  
例えば、同一アルファベットの文字列32バイト(256ビット)である`bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb`をECBで暗号化する。  
すると16バイト(128ビット)ブロック(`bbbbbbbbbbbbbbbb`と`bbbbbbbbbbbbbbbb`)ごとに暗号化された暗号文ブロックが二つ生成されるが、これが一致する。  
同一でないアルファベット`baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`である場合には、`baaaaaaaaaaaaaaa`と`aaaaaaaaaaaaaaaa`のブロックに分けられるため暗号文ブロックが一致しない。  
つまり暗号化結果の前半と後半が一致した場合、入力のすべてのアルファベットが同一であるといえる。  
あとはその時のパディングを`rand_printable`の順番から求めてやれば、先頭に位置しているフラグの文字も分かる。  
以下のsolve.pyで行う。  
```python
import os
import random
import string

random.seed(int(os.path.getmtime("ciphertext")))
rand_printable = [x for x in string.printable]
random.shuffle(rand_printable)

with open("ciphertext") as f:
    ciphertext = f.read()
    ciphertext = [ciphertext[i : i + 64] for i in range(0, len(ciphertext), 64)]
    ciphertext = [ciphertext[i : i + 100] for i in range(0, len(ciphertext), 100)]

flag = ""
for clist in ciphertext:
    for i in range(len(clist)):
        if clist[i][:32] == clist[i][32:]:
            flag += rand_printable[i]
            break

print(flag)
```
実行する。  
```bash
$ python solve.py
brck{EZP3n9u1nZ}
```
flagが得られた。  

## brck{EZP3n9u1nZ}
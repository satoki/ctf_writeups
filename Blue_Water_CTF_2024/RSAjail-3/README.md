# RSAjail-3:Misc:165pts
Let's learn about RSA!  

`nc rsajail3.chal.perfect.blue 1337`  

[chall.py](chall.py)  

# Solution
接続先とソースが配布される。  
ソースは以下の通りであった。  
```python
from subprocess import Popen, PIPE, DEVNULL
from Crypto.Util.number import getPrime
from secret import fname, flag
import time, string, secrets, os

def keygen():
    pr = Popen(['python3', '-i'], stdin=PIPE, stdout=DEVNULL, stderr=DEVNULL, text=True, bufsize=1)

    p, q = getPrime(1024), getPrime(1024)
    N, e = p * q, 0x10001
    m = secrets.randbelow(N)
    c = pow(m, e, N)

    pr.stdin.write(f"{(N, p, c) = }\n")
    pr.stdin.write(f"X = lambda m: open('{fname}', 'w').write(str(m))\n")
    # X marks the spot!
    
    return pr, m

def verify(pr, m, msg):
    time.sleep(1)

    assert int(open(fname, 'r').read()) == m
    os.remove(fname)
    pr.kill()

    print(msg)

# Example!
pr, m = keygen()
example = [
    "q = N // p",
    "phi = (p - 1) * (q - 1)",
    "d = pow(0x10001, -1, phi)",
    "m = pow(c, d, N)",
    "X(m)"
]

for code in example:
    pr.stdin.write(code + '\n')

verify(pr, m, "I showed you how RSA works, try yourself!")


# Your turn!
pr, m = keygen()
while code := input(">>> "):
    if (len(code) > 3) or any(c == "\\" or c not in string.printable for c in code):
        print('No hack :(')
        continue
    pr.stdin.write(code + '\n')

verify(pr, m, flag)
```
初めに`keygen`が呼ばれ、内部で`p`、`q`、`m`を生成して利用し、RSAで`m`を暗号化した`c`を計算している(`N`は`p * q`、`e`は`0x10001`)。  
`Popen`で`python3 -i`も実行しており、値の入った変数`N`、`p`、`c`と、ファイル`fname`に値を書き込むラムダ式である`X = lambda m: open('{fname}', 'w').write(str(m))`を利用できる状態にしている。  
その後に、ユーザの入力した任意のコードを複数行実行できるが、出力は`DEVNULL`に設定されており何も得られない。  
また、1行に3文字までの`string.printable`である必要もあり、行末には必ず改行が挿入される。  
フラグが得られる条件は、`m`が`fname`に書かれていることである。  
まとめると、値の入った変数`N`、`p`、`c`とファイル書き込み機能`X`が利用できる出力のない環境で、1行3文字のpythonコードを書いて`c`を`m`に復号し、`X(m)`を呼び出してファイルに書き込めということらしい。  
ソース中に以下のようなexampleも用意されている。  
```python
example = [
    "q = N // p",
    "phi = (p - 1) * (q - 1)",
    "d = pow(0x10001, -1, phi)",
    "m = pow(c, d, N)",
    "X(m)"
]
```
これを1行3文字に変形すればよい。  
`()`を用いることで、代入時の右辺に改行を含めることができると気付く。  
以下のように行う。  
```python
q=(
N
//
p
)
h=(
(
p-1
)
*
(
q-1
)
)
d=(
pow
(
(2
<<
15)
+1
,
-1
,
h
)
)
m=(
pow
(
c
,
d
,
N
)
)
(
X
(
m
)
)
```
見やすく直すと次のようになる。  
```python
q=(N//p)
h=((p-1)*(q-1))
d=(pow((2<<15)+1,-1,h))
m=(pow(c,d,N))
(X(m))
```
これを以下のようにサーバへ送信する(proof-of-workに注意)。  
```bash
$ nc rsajail3.chal.perfect.blue 1337
== proof-of-work: enabled ==
please solve a pow first
You can run the solver with:
    python3 <(curl -sSL https://goo.gle/kctf-pow) solve s.ADQ6.AABGKa0lYTAUtJmjU0K5HdJv
===================

Solution? s.AABs6ZwjPFd44ym3QG4/qS/dww1JwDPTuuTNb7eZQoCH5EhwFL5vJR9mh8tzhwzAzoVvCDZgbXTg3z1egyqr+iaXRvjN2jTMSGY5cCBx7m/8OWzsmmTByDMaHIAI9Uy5nc9ZV8UyBHrP36LQ4+jO+tvpo2sfZgFyk77QOPmw/jMdxa6J09RqguHrNDr3kILh2sndCdjMSQH/p9GJ74Qw0bTV
Correct
__________  _________   _____       __       .__.__            ________
\______   \/   _____/  /  _  \     |__|____  |__|  |           \_____  \
 |       _/\_____  \  /  /_\  \    |  \__  \ |  |  |    ______   _(__  <
 |    |   \/        \/    |    \   |  |/ __ \|  |  |__ /_____/  /       \
 |____|_  /_______  /\____|__  /\__|  (____  /__|____/         /______  /
        \/        \/         \/\______|    \/                         \/

I showed you how RSA works, try yourself!
>>> q=(
>>> N
>>> //
>>> p
>>> )
>>> h=(
>>> (
>>> p-1
>>> )
>>> *
>>> (
>>> q-1
>>> )
>>> )
>>> d=(
>>> pow
>>> (
>>> (2
>>> <<
>>> 15)
>>> +1
>>> ,
>>> -1
>>> ,
>>> h
>>> )
>>> )
>>> m=(
>>> pow
>>> (
>>> c
>>> ,
>>> d
>>> ,
>>> N
>>> )
>>> )
>>> (
>>> X
>>> (
>>> m
>>> )
>>> )
>>>

bwctf{Lmao_pow_function_is_too_powerful...Time_to_ban_it!!!!}
```
flagが得られた。  

## bwctf{Lmao_pow_function_is_too_powerful...Time_to_ban_it!!!!}
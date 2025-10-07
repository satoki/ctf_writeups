# Easy Jail:Misc:311pts
`nc misc-b6c94dd8.p1.securinets.tn 7000`  

[give.py](give.py)  

# Solution
接続先とソースコードが渡される。  
give.pyは以下の通りであった。  
```py
import random
import string

seed = random.randint(0, 2**20)
shift_rng = random.Random(seed)

class ProtectedFlag:
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return "variable protected, sryy"

    def __repr__(self):
        return "variable protected, sryy"

    def __getitem__(self, index):
        try:
            return self._value[index]
        except Exception:
            return "variable protected, sryy"

# Example flag
flag = ProtectedFlag("flag{dummy_flag}")

def shift_mapping(mapping):
    # well guess how it was done >_<

def make_initial_mapping():
    letters = list(string.ascii_lowercase)
    shuffled = letters[:]
    random.shuffle(shuffled)
    return dict(zip(letters, shuffled))

def main():
    valid_chars = set(string.ascii_lowercase + "[]()~><*+")
    mapping = make_initial_mapping()
    print("Welcome to the shifting jail! Enter text using only a-z, []()~><*+")

    try:
        while True:
            user_in = input("> ").strip()
            if len(user_in) > 150:
                raise ValueError(f"Input exceeds 150 characters")

            if not all(c in valid_chars for c in user_in):
                print("Invalid input. Only [a-z] and []()~><*+ are allowed.")
                continue

            encoded = "".join(mapping[c] if c in mapping else c for c in user_in)

            mapping = shift_mapping(mapping)
            try:
                result = eval(encoded, {"__builtins__": None}, {"flag": flag})
                print(result)
            except Exception:
                print(encoded)

    except KeyboardInterrupt:
        print("\nGoodbye!")

if __name__ == "__main__":
    main()
```
ユーザ入力を150文字まで受け取り`eval`するようだが、`a-z`と`[]()~><*+`の文字種制限がある。  
受け取った入力には非公開ルールでシフトが実施されるようで、ルール自体をGuessする必要がありそうだ。  
さらに、ビルトインがすべて消されており、変数`flag`にだけフラグがある環境でのコード実行となる。  
変数の中身を取り出せということのようだ。  
ただし、`flag`は以下の通り、`ProtectedFlag`クラスで特殊メソッドが上書きされている。  
```py
class ProtectedFlag:
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return "variable protected, sryy"

    def __repr__(self):
        return "variable protected, sryy"

    def __getitem__(self, index):
        try:
            return self._value[index]
        except Exception:
            return "variable protected, sryy"

# Example flag
flag = ProtectedFlag("flag{dummy_flag}")
```
これにより、変数を`eval("flag")`のようにそのまま評価してもフラグは帰ってこず、`flag[0]`のようなアクセスか、`flag._value`のような取得が必要となる。  
後者は`_`が禁止されているので前者を目指すが、数字が利用できない。  
ここで、`flag[[]>[[]]]`は`flag[False]`となり`flag[0]`と等価、`flag[[]<[[]]]`は`flag[True]`となり`flag[1]`と等価なことに気づく。  
さらに`flag[([]<[[]])+([]<[[]])]`は`flag[2]`というように、加算により数値を増やすことができる。  
これでフラグを一文字ずつ取得できそうだ。  
残るはシフトされるルールだが、同じ文字でも毎回違う値にシフトされる。  
一見すると予測不可能だが、複数回実行するとある地点で同じルールが適用されることがあるとわかる。  
```bash
$ nc misc-b6c94dd8.p1.securinets.tn 7000
Welcome to the shifting jail! Enter text using only a-z, []()~><*+
> aabbcc
aabbcc
ddjjbb
> aabbcc
aabbcc
cciiaa
> aabbcc
aabbcc
bbhhzz
> aabbcc
aabbcc
aaggyy
> aabbcc
aabbcc
bbhhzz
```
つまり、最初に`abcdefghijklmnopqrstuvwxyz`のルールのうち一つを記録しておき、それが適用されるまで何度も試行すればよい。  
コードが実行できた場合は、フラグの一文字だけが返されるので判定も容易だ。  
以下のようなsolve.pyで一文字ずつフラグを取得する(数値部分は文字数制限に注意しながら、LLMに書かせた)。  
```py
import sys
from ptrlib import *

num = [
    "([]>[[]])",  # 0
    "([]<[[]])",  # 1
    "([]<[[]])+([]<[[]])",  # 2
    "([]<[[]])+([]<[[]])+([]<[[]])",  # 3
    "(([]<[[]])+([]<[[]]))**(([]<[[]])+([]<[[]]))",  # 4 = 2^2
    "([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])",  # 5
    "(([]<[[]])+([]<[[]])+([]<[[]]))*(([]<[[]])+([]<[[]]))",  # 6 = 3*2
    "(([]<[[]])+([]<[[]])+([]<[[]]))*(([]<[[]])+([]<[[]]))+([]<[[]])",  # 7 = 3*2+1
    "(([]<[[]])+([]<[[]]))**(([]<[[]])+([]<[[]])+([]<[[]]))",  # 8 = 2^3
    "(([]<[[]])+([]<[[]])+([]<[[]]))**(([]<[[]])+([]<[[]]))",  # 9 = 3^2
    "(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))*(([]<[[]])+([]<[[]]))",  # 10 = 5*2
    "(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))*(([]<[[]])+([]<[[]]))+([]<[[]])",  # 11 = 5*2+1
    "(([]<[[]])+([]<[[]])+([]<[[]]))*(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))",  # 12 = 3*4
    "(([]<[[]])+([]<[[]])+([]<[[]]))*(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))+([]<[[]])",  # 13 = 3*4+1
    "(([]<[[]])+([]<[[]]))*(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))",  # 14 = 2*7
    "(([]<[[]])+([]<[[]])+([]<[[]]))*(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))",  # 15 = 3*5
    "(([]<[[]])+([]<[[]]))**(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))",  # 16 = 2^4
    "(([]<[[]])+([]<[[]]))**(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))+([]<[[]])",  # 17 = 2^4+1
    "(([]<[[]])+([]<[[]])+([]<[[]]))*(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))",  # 18 = 3*6
    "(([]<[[]])+([]<[[]])+([]<[[]]))*(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))+([]<[[]])",  # 19 = 3*6+1
    "(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))*(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))",  # 20 = 4*5
    "(([]<[[]])+([]<[[]])+([]<[[]]))*(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))",  # 21 = 3*7
    "(([]<[[]])+([]<[[]]))*(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))",  # 22 = 2*11
    "(([]<[[]])+([]<[[]]))*(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))+([]<[[]])",  # 23 = 2*11+1
    "(([]<[[]])+([]<[[]])+([]<[[]]))*(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))",  # 24 = 3*8
    "(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))**(([]<[[]])+([]<[[]]))",  # 25 = 5^2
    "(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))**(([]<[[]])+([]<[[]]))+([]<[[]])",  # 26 = 5^2+1
    "(([]<[[]])+([]<[[]])+([]<[[]]))**(([]<[[]])+([]<[[]])+([]<[[]]))",  # 27 = 3^3
    "(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))*(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))",  # 28 = 4*7
    "(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))*(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))+([]<[[]])",  # 29 = 4*7+1
    "(([]<[[]])+([]<[[]])+([]<[[]]))*(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))",  # 30 = 3*10
    "(([]<[[]])+([]<[[]])+([]<[[]]))*(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))+([]<[[]])",  # 31 = 3*10+1
    "(([]<[[]])+([]<[[]]))**(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))",  # 32 = 2^5
    "(([]<[[]])+([]<[[]]))**(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))+([]<[[]])",  # 33 = 2^5+1
    "(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))**(([]<[[]])+([]<[[]]))-(([]<[[]])+([]<[[]]))",  # 34 = 6^2-2
    "(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))*(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))",  # 35 = 7*5
    "(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))**(([]<[[]])+([]<[[]]))",  # 36 = 6^2
    "(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))**(([]<[[]])+([]<[[]]))+([]<[[]])",  # 37 = 6^2+1
    "(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))**(([]<[[]])+([]<[[]]))+(([]<[[]])+([]<[[]]))",  # 38 = 6^2+2
    "(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))**(([]<[[]])+([]<[[]]))+(([]<[[]])+([]<[[]])+([]<[[]]))",  # 39 = 6^2+3
    "(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))*(([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]])+([]<[[]]))",  # 40 = 4*10
]

logger.setLevel("CRITICAL")

FLAG = ""

for i in num[len(FLAG) :]:

    sock = Socket("nc misc-b6c94dd8.p1.securinets.tn 7000")

    sock.sendlineafter(b"> ", "abcdefghijklmnopqrstuvwxyz")
    _ = sock.recvline()
    shifted = sock.recvline().decode()
    conv = str.maketrans(shifted, "abcdefghijklmnopqrstuvwxyz")

    code = f"flag[{i}]".translate(conv)

    while True:
        sock.sendlineafter(b"> ", code)
        _ = sock.recvline()
        res = sock.recvline().decode()
        if len(res) == 1:
            FLAG += res
            print(f"FLAG: {FLAG}")
            if res == "}":
                sys.exit(0)
            sock.close()
            break
```
実行する。  
```bash
$ python solve.py
FLAG: S
FLAG: Se
FLAG: Sec
FLAG: Secu
FLAG: Secur
FLAG: Securi
FLAG: Securin
FLAG: Securine
FLAG: Securinet
FLAG: Securinets
FLAG: Securinets{
FLAG: Securinets{H
FLAG: Securinets{H0
FLAG: Securinets{H0p
FLAG: Securinets{H0p3
FLAG: Securinets{H0p3_
FLAG: Securinets{H0p3_Y
FLAG: Securinets{H0p3_Y0
FLAG: Securinets{H0p3_Y0u
FLAG: Securinets{H0p3_Y0u_
FLAG: Securinets{H0p3_Y0u_L
FLAG: Securinets{H0p3_Y0u_L0
FLAG: Securinets{H0p3_Y0u_L0S
FLAG: Securinets{H0p3_Y0u_L0ST
FLAG: Securinets{H0p3_Y0u_L0ST_
FLAG: Securinets{H0p3_Y0u_L0ST_1
FLAG: Securinets{H0p3_Y0u_L0ST_1t
FLAG: Securinets{H0p3_Y0u_L0ST_1t!
FLAG: Securinets{H0p3_Y0u_L0ST_1t!}
```
flagが得られた。  

## Securinets{H0p3_Y0u_L0ST_1t!}
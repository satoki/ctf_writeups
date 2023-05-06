# Guess:Misc:236pts
Guess the numbers 🤔  
`nc guess-mis.wanictf.org 50018`  

[mis-guess.zip](mis-guess.zip)  

# Solution
接続先とソースが渡される。  
ソースは以下の通りであった。  
```python
import os
import random

ANSWER = list(range(10**4))
random.shuffle(ANSWER)
CHANCE = 15


def peep():
    global CHANCE
    if CHANCE <= 0:
        print("You ran out of CHANCE. Bye!")
        exit(1)
    CHANCE -= 1

    index = map(int, input("Index (space-separated)> ").split(" "))
    result = [ANSWER[i] for i in index]
    random.shuffle(result)

    return result


def guess():
    guess = input("Guess the numbers> ").split(" ")
    guess = list(map(int, guess))
    if guess == ANSWER:
        flag = os.getenv("FLAG", "FAKE{REDACTED}")
        print(flag)
    else:
        print("Incorrect")


def main():
    menu = """
    1: peep
    2: guess""".strip()
    while True:
        choice = int(input("> "))
        if choice == 1:
            result = peep()
            print(result)
        elif choice == 2:
            guess()
        else:
            print("Invalid choice")
            break
```
`list(range(10**4))`をシャッフルして、それを当てるゲームのようだ。  
15回だけ`peep()`で指定したindexのリストの中身を読み取れる。  
ただし返ってくるリストもシャッフルされているため、複数個読み取っても元のindexがわからない。  
ここで、`peep()`で複数回同じindexを指定できることに気づく。  
試しに`0 1 1 2 2 2`とすると、`[8421, 2273, 2273, 2273, 8421, 9197]`が返ってきた。  
シャッフルされるものの個数で元のindexを当てることができる(ここでは9197が0、8421が1、2273が2)。  
以下のいい加減なguess.pyで当てる。  
```python
import collections
from pwn import *

context.log_level = "error"

ANSWER = ["-1"] * 10**4

p = remote("guess-mis.wanictf.org", 50018)

index = 0
while index < 10**4:
    p.recvuntil(b"> ")
    p.sendline(b"1")
    p.recvuntil(b"index> ")
    payload = []
    for i in range(index, index + 1000):
        for _ in range((i % 1000) + 1):
            payload.append(f"{i}")
    payload = " ".join(payload)
    # print(payload) #Debug
    p.sendline(payload.encode())
    resp = collections.Counter(eval(p.recvline().decode())).most_common()
    for i in range(index, index + 1000):
        ANSWER[i] = f"{resp[-((i % 1000) + 1)][0]}"
    # print(ANSWER) #Debug
    index += 1000
    print(f"{index}/{10**4}")

p.recvuntil(b"> ")
p.sendline(b"2")
p.recvuntil(b"Guess the list> ")
p.sendline((" ".join(ANSWER)).encode())

p.interactive()
```
実行する。  
```bash
$ python guess.py
1000/10000
2000/10000
3000/10000
4000/10000
5000/10000
6000/10000
7000/10000
8000/10000
9000/10000
10000/10000
FLAG{How_did_you_know?_10794fcf171f8b2}

1: peep
2: guess
> $
```
当たってflagが得られた。  

## FLAG{How_did_you_know?_10794fcf171f8b2}
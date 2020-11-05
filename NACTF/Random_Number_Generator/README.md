# Random Number Generator:Cryptography:250pts
Dr. J created a fast pseudorandom number generator (prng) to randomly assign pairs for the upcoming group test. Austin really wants to know the pairs ahead of time... can you help him and predict the next output of Dr. J's prng?  
nc challenges.ctfd.io 30264  
Hint  
Check out the hint for "Dr. J's Vegetable Factory #2 🥕" to see an example of how to connect to the server with code.  
[rand0.py](rand0.py)  

# Solution
rand0.pyによって乱数が生成されているようだ。  
rand0.pyは以下のようになっている。  
```python:rand0.py
try:
    with open("flag.txt", "r") as fin:
        flag = fin.read()
except:
    print("Problem is misconfigured - ping us on discord if this is happening on the shell server")
    exit()

import random, time
random.seed(round(time.time() / 100, 5))

print("Welcome to Dr. J's Random Number Generator!")
print("[r] Print a new random number")
print("[g] Guess the next two random numbers and receive the flag!")
print("[q] Quit")


while True:
    inp = input("\n> ")
    if inp == "r":
        print(random.randint(1, 100000000))
    elif inp == "g":
        print("Guess the next two random numbers for a flag!\nGood luck!\nEnter your first guess:")
        if input("> ") == str(random.randint(1, 100000000)):
            print("Wow, lucky guess... You won't be able to guess right a second time\nEnter your second guess:")
            if input("> ") == str(random.randint(1, 100000000)):
                print("What? You must have psychic powers... Well here's your flag: ")
                print(flag)
                break
            else:
                print("That's incorrect. Get out of here!")
                break
        else:
            print("That's incorrect. Get out of here!")
            break
    elif inp == "q":
        print("Goodbye!")
        break
```
以下に注目する。  
```python
~~~
import random, time
random.seed(round(time.time() / 100, 5))
~~~
    inp = input("\n> ")
    if inp == "r":
        print(random.randint(1, 100000000))
    elif inp == "g":
        print("Guess the next two random numbers for a flag!\nGood luck!\nEnter your first guess:")
        if input("> ") == str(random.randint(1, 100000000)):
            print("Wow, lucky guess... You won't be able to guess right a second time\nEnter your second guess:")
            if input("> ") == str(random.randint(1, 100000000)):
                print("What? You must have psychic powers... Well here's your flag: ")
                print(flag)
                break
~~~
```
シード値`round(time.time() / 100, 5)`で`random.randint(1, 100000000)`を呼んでいる。  
シードがわかれば、乱数が予測可能だ。  
時間を使っているため、総当たり可能である。  
以下のyosoku.pyを用いる。  
```python:yosoku.py
import random, time

i = input(">")
s = round(time.time() / 100, 5)
print("[{}]".format(s))

while True:
    s = round(s - 0.00001, 5)
    random.seed(s)
    #print(s)
    if str(random.randint(1, 100000000)) == i:
        print(random.randint(1, 100000000))
        print(random.randint(1, 100000000))
        break
```
次の手順でシードを予測し、乱数を生成する。  
    1.ncでサーバへ接続する  
    2.yosoku.pyを実行する  
    3."r"を入力しサーバから一つ目の乱数を取得する  
    4.yosoku.pyへ3から得た乱数を入力する  
各ステップごとに停止してもよいが、別ターミナルで行うと分かりやすい(1.と3.、2.と4.)。  
実行結果は以下になる。  
```bash
$ nc challenges.ctfd.io 30264
Welcome to Dr. J's Random Number Generator!
[r] Print a new random number
[g] Guess the next two random numbers and receive the flag!
[q] Quit

> ^Z
[1]+  停止                  nc challenges.ctfd.io 30264
$ python yosoku.py
>^Z
[2]+  停止                  python3 yosoku.py
$ fg 1
nc challenges.ctfd.io 30264
r
88458458

> ^Z
[1]+  停止                  nc challenges.ctfd.io 30264
$ fg 2
python3 yosoku.py
88458458
[16043012.01759]
12165510
55785909
$ fg 1
nc challenges.ctfd.io 30264
g
Guess the next two random numbers for a flag!
Good luck!
Enter your first guess:
> 12165510
Wow, lucky guess... You won't be able to guess right a second time
Enter your second guess:
> 55785909
What? You must have psychic powers... Well here's your flag:
nactf{ch000nky_turn1ps_1674973}
```

## nactf{ch000nky_turn1ps_1674973}
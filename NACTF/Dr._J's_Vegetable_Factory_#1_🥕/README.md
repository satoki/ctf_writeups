# Dr. J's Vegetable Factory #1 🥕:General Skills:50pts
After years of collecting plush vegetable toys, Dr. J decided to take on his true passion: starting a vegetable factory. Dr. J is incredibly organized, so he likes all of his vegetables to be in the proper order. In fact, he built a robot "Turnipinator-1000" to alphabetize his vegetables for him! Unfortunately, Dr. J doesn't know what instructions to give Turnipinator-1000. Can you help him out? 🥬🥕🌽🍆🥦🥒🥑🍄  
nc challenges.ctfd.io 30267  
Give instructions in the form of numbers separated by spaces. Entering the number x will swap the vegetable in position x with the vegetable in position x+1. Positions start at zero, not one. (Dr. J is a programmer after all.) For example, given the following vegetables: Avocado, Brocolli, Eggplant, Daikon Radish, Carrot, one possible solution is "3 2 3"  
Avocado, Brocolli, Eggplant, Daikon Radish, Carrot  
    1.(swap 3 and 4)  
Avocado, Brocolli, Eggplant, Carrot, Daikon Radish  
    2.(swap 2 and 3)  
Avocado, Brocolli, Carrot, Eggplant, Daikon Radish  
    3.(swap 3 and 4)  
Avocado, Brocolli, Carrot, Daikon Radish, Eggplant  
Hint  
Try sorting the vegetables by hand! For example: [insertion sort](https://www.geeksforgeeks.org/insertion-sort/).  

# Solution
接続すると野菜が並べられるので、swap手順を送信すればいいようだ。  
以下のTheVeryHungryCaterpillar.pyで自動化する。  
```python:TheVeryHungryCaterpillar.py
from pwn import *

io = remote("challenges.ctfd.io", 30267)

def bs(text):
    nums = ""
    for i in range(len(text)):
        for j in range(len(text)-1, i, -1):
            if text[j] < text[j-1]:
                text[j], text[j-1] = text[j-1], text[j]
                nums += "{} ".format(j-1)
    print(nums[:-1])
    return nums[:-1]

for i in range(3):
    print(io.recvline().decode("utf-8"))

io.sendline("1")

for i in range(4):
    print(io.recvline().decode("utf-8"))
text = io.recvline().decode("utf-8").replace("\n","").split(", ")
print(text)
for i in range(3):
    print(io.recvline().decode("utf-8"))
io.sendline(bs(text))

while True:
    try:
        for i in range(5):
            print(io.recvline().decode("utf-8"))
        text = io.recvline().decode("utf-8").replace("\n","").split(", ")
        print(text)
        io.sendline(bs(text))
        print(io.recvline().decode("utf-8"))
    except:
        break
```
実行する。  
```bash
$ python TheVeryHungryCaterpillar.py
~~~
nactf{1f_th3r3s_4_pr0b13m_13ttuce_kn0w_db4d736fd28f0ea39ec}
```

## nactf{1f_th3r3s_4_pr0b13m_13ttuce_kn0w_db4d736fd28f0ea39ec}
# Dr. J's Vegetable Factory #3 🥕:General Skills:175pts
Rahul hates vegetables. Rahul hates vegetables so much that he snuck into Dr. J's factory at night to sabotage Dr. J's vegetable production! He brought a sledgehammer and broke the wheels of Dr. J's robot! 😓 Now the robot is stuck in place, and instead of being able to swap any adjacent elements, it can only swap the elements in positions 0 and 1!  
But Dr. J won't let this incident stop him from giving the people the vegetables they deserve! Dr. J is a problem solver 🧠. He organized his vegetables in a circle, and added a conveyor-belt that allows him shift the positions of the vegetables. He thinks that the conveyor belt should make it possible to sort his vegetables, but he's not 100% sure. Can you help him out?  
nc challenges.ctfd.io 30267  
Enter letters separated by spaces to sort Dr. J's vegetables. Entering "c" will activate the conveyor belt and shift all vegetables left one position. Entering "s" will swap the vegetable in position 0 with the vegetable in position 1.  
Hint  
This problem boils down to the same thing as #2. Try bubble sort!  

# Solution
[Dr. J's Vegetable Factory #1 🥕](../Dr._J's_Vegetable_Factory_#1_🥕)や[Dr. J's Vegetable Factory #2 🥕](../Dr._J's_Vegetable_Factory_#2_🥕)と同じようだ。  
TheVeryHungryCaterpillar.pyを編集した、以下のTheVeryHungryCaterpillar3.pyで自動化する。  
```python:TheVeryHungryCaterpillar3.py
from pwn import *

io = remote("challenges.ctfd.io", 30267)

def bs(text):
    nums = ""
    for i in range(len(text)):
        for j in range(len(text) - i - 1):
            if text[j] > text[j + 1]:
                text[j], text[j + 1] = text[j + 1], text[j]
                nums += "s "
            nums += "c "
        nums += "c " * (i+1)
    #print(nums[:-1])
    return nums[:-1]

for i in range(3):
    print(io.recvline().decode("utf-8"))

io.sendline("3")

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
$ python TheVeryHungryCaterpillar3.py
~~~
nactf{1t_t4k35_tw0_t0_m4n90_8a51c7b47fbe227}
```

## nactf{1t_t4k35_tw0_t0_m4n90_8a51c7b47fbe227}
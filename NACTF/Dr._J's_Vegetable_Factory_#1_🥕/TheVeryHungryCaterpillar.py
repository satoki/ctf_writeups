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
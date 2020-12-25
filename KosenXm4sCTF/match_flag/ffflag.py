import pwn

flag = ""

while True:
    for i in "abcdefghijklmnopqrstuvwxyz0123456789{}_ ":
        io = pwn.remote("27.133.155.191", 30009)
        io.sendline(flag+i)
        if b"Correct!!!" in io.recv():
            flag += i
            break
        io.close()
    if "}" in flag:
        print(flag)
        break
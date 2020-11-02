flag = open("enc.txt").read()
msg = 101

msglen = int(len(flag)/msg)
msgs = [[]] * msg

for i in range(msg):
    msgs[i] = flag[:msglen]
    flag = flag[msglen:]

for i in range(msglen):
    zero = 0
    for j in range(msg):
        if msgs[j][i] == "0":
            zero += 1
    if (msg/2) < zero:
        print(0, end="")
    else:
        print(1, end="")
print()
import re

f = open("autorev_assemble.txt")
text = f.read()

fxxx = []
for s in re.finditer("callq.*?<(?P<fn>f[0-9]*?)>", text):
    fxxx.append(s.group("fn"))
#print(len(fxxx))
table = []
for t in re.finditer("<f[0-9](.|\s)*?retq", text):
    u = t.group()
    fn = re.match("<(?P<fn>f[0-9]*?)>", u)
    fi = fn.group("fn")
    pos = re.search("add(.|\s)*?0x(?P<pos>.*?),", u)
    if pos != None:
        se = pos.group("pos")
    else:
        se = "0"
    cha = re.search("cmp(.|\s)*?0x(?P<cha>.*?),", u)
    if cha != None:
        th = cha.group("cha")
    else:
        th = "0"
    table.append([fi, int(se, 16), int(th, 16)])
flag = ['@'] * len(fxxx)
for i in range(len(fxxx)):
    for j in range(len(table)):
        if fxxx[i] == table[j][0]:
            flag[table[j][1]] = chr(table[j][2])
print("".join(flag))

f.close()
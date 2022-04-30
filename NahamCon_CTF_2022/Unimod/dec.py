out = open("out", "r").read()
k = ord(out[0]) - ord("f")
flag = ""

for c in out:
    flag += chr(ord(c) - k)

print(flag)
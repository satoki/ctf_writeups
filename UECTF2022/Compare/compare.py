org = open("UECTF_org.bmp", "rb").read()
new = open("UECTF_new.bmp", "rb").read()

for i in range(len(org)):
    if org[i] != new[i]:
        print(chr(new[i]), end="")
import os
import random
import string

random.seed(int(os.path.getmtime("ciphertext")))
rand_printable = [x for x in string.printable]
random.shuffle(rand_printable)

with open("ciphertext") as f:
    ciphertext = f.read()
    ciphertext = [ciphertext[i : i + 64] for i in range(0, len(ciphertext), 64)]
    ciphertext = [ciphertext[i : i + 100] for i in range(0, len(ciphertext), 100)]

flag = ""
for clist in ciphertext:
    for i in range(len(clist)):
        if clist[i][:32] == clist[i][32:]:
            flag += rand_printable[i]
            break

print(flag)
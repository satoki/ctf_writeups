import sys

chars = '0123456789W!"#%&()*+,-./:;<=>?@_{|}'
new_chars = ""

if len(sys.argv) != 1:
    chars += sys.argv[1]


for i in chars:
    for j in chars:
        #And
        c = chr(ord(i) & ord(j))
        if (not c in chars) and (not c in new_chars) and (c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            print("(\"{}\"%26\"{}\"):{}".format(i, j, c))
            new_chars += c
        #Or
        c = chr(ord(i) | ord(j))
        if (not c in chars) and (not c in new_chars) and (c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            print("(\"{}\"%7C\"{}\"):{}".format(i, j, c))
            new_chars += c

print(new_chars)
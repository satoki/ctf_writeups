key = ""
flag = open("output.txt").read()

def encrypt(s1, s2):
    assert len(s1) == len(s2)

    result = ""
    for c1, c2 in zip(s1, s2):
        result += chr(ord(c1) ^ ord(c2))
    return result

for i in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
    for j in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
        for k in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
            key = (i + j + k) * 19
            ciphertext = encrypt(flag, key)
            if "FLAG{" in ciphertext:
                print(ciphertext)
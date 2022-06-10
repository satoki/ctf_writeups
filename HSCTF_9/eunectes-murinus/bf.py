bullets = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_"

for b1 in bullets:
    for b2 in bullets:
        for b3 in bullets:
            i = ord(b1)
            j = ord(b2)
            k = ord(b3)
            if i * 8 * (j - 4) * (k + 4) == 9711352:
                print(b1, b2, b3)
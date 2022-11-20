def xor(data, key):
    return bytearray(a^b for a, b in zip(*map(bytearray, [data, key])))

prefix = b"UECTF{"
cflag = open("flag.jpg", "rb").read()

flag = xor(cflag, prefix * int(len(cflag) / len(prefix) + 1))
open("satoki.jpg", "wb").write(flag)
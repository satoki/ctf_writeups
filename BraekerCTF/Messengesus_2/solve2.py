with open("ciphertext", "rb") as f:
    data = f.read()

for flag_len in range(1, len(data)):
    flag = ""
    if len(data) % flag_len:
        continue
    cflags = [data[x : x + flag_len] for x in range(0, len(data), flag_len)]
    for i in range(flag_len):
        clist = [chr(f[i] ^ 0x0A) for f in cflags]
        c = "".join(set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?_{}") - set(clist))
        flag += c
    if "brck{" in flag:
        print(f"flag_len: {flag_len}")
        print(flag)
        break
from cipher import STREAM

with open("output.txt", "r") as f:
    output = f.read()

encflag = bytes.fromhex(output.replace("encrypted flag > ", ""))
for seed in range(0xFFFF):
    stream = STREAM(seed, 16)
    decflag = stream.decrypt(encflag)
    if b"DH{" in decflag:
        print(f"seed = {seed}")
        print(f"flag = {decflag.decode()}")
        break

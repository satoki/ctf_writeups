import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor

alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def flag(text):
    res = subprocess.check_output("./a.out", input=b"HarekazeCTF{ID" + text.encode() + b"X}")
    print(text)
    sys.stdout.flush()
    if not b"Wrong flag" in res:
        print("\033[31m", end="")
        print("{} : {}".format(text, res))
        sys.stdout.flush()

tpe = ThreadPoolExecutor(max_workers=100)

i1 = input("[1]>> ")
print(i1)
for i2 in alph:
    for i3 in alph:
        for i4 in alph:
            tpe.submit(flag, "{}{}{}{}".format(i1, i2, i3, i4))

tpe.shutdown()
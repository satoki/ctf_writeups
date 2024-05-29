import sys
import random

payload = sys.argv[1]
rand_payload = list(" " * len(payload))

for i in range(len(payload)):
    tmp = list(" " * len(payload))
    tmp[i] = "\x00"
    random.seed(0)
    random.shuffle(tmp)
    rand_payload[i] = payload[tmp.index("\x00")]

print("".join(rand_payload))
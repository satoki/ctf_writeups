# http://ctf.publog.jp/archives/1056626672.htmlより
import sys
import matplotlib.pyplot as plt

plt.xlim(-100, 2000)
plt.ylim(-100, 500)

filename = "capdata.txt"

def compliment(h):
    i = int(h, 16)
    return i - ((0x80 & i) << 1)

def plot(i, x, y, c="red"):
    plt.plot(x, y, color=c, marker="o")

tx = ty = i = 0

for line in open(filename).readlines():
    if len(line) > 1:
        status, dx, dy, junk, aaa, bbb, ccc, ddd = line.split(":")
        tx += compliment(dx)
        ty += compliment(dy)
    if status != "00":
        i += 1
        plot(i, tx, ty)

plt.show()
import re
import socket
import numpy as np

def fib(n):
    f = (((1 + np.sqrt(5)) / 2)**n - ((1 - np.sqrt(5)) / 2)**n ) / np.sqrt(5)
    return int(f)

def rot(d, s):
    s = s % 26
    r = []
    for c in d:
        c = ord(c)
        c = c + s
        if c > 90:
            c = c - 26
        r.append(chr(c))
    r = "".join(r)
    return r

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("misc.2020.chall.actf.co", 20300))

while True:
    rtext = str(s.recv(512))
    if "actf" in rtext:
        print(rtext)
        break
    #print(rtext)
    se = re.search(".*Shift\s(?P<t>.*)\sby\sn=(?P<n>[0-9]*).*", rtext)
    text = se.group("t")
    #print(text)
    num = int(se.group("n"))
    #print(num)
    ans = rot(text, fib(num))
    #print(ans)
    s.sendall((ans+"\n").encode("utf-8"))

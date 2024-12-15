import itertools
from unicodedata import numeric


# server.py
def calc(s):
    if (loc := s.find("+")) != -1:
        return calc(s[:loc]) + calc(s[loc + 1 :])
    if (loc := s.find("*")) != -1:
        return calc(s[:loc]) * calc(s[loc + 1 :])
    x = 0
    for c in s:
        x = 10 * x + numeric(c)
    return x


chars = {}
for i in range(0xFFFFF):
    try:
        c = chr(i)
        if (c).isnumeric():
            if numeric(c) not in chars:
                chars[int(numeric(c))] = c
    except:
        pass

chars = list(chars.values())
chars.append("+")
chars.append("*")

permutations = ["".join(p) for p in itertools.permutations(chars, 4)]
for p in permutations:
    if abs(1234567 - calc(p)) < 5:
        print(f"FOUND: raw: {p}")
        print(f"<num: {calc(p)}, diff: {1234567 - calc(p)}>")

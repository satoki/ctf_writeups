text = "xn4u{fejyhzwyjazwzqkszurwhyqaop}"
n = 26

for i in text:
    if n <= 0:
        n = 26
    if not i in "4{}":
        i = chr((ord(i) - ord('a') + n) % 26 + ord('a'))
        n -= 1
    print(i, end="")
print()
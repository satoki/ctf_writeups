from sympy import sieve

p = 1#BOM
MAXP = 100000
s = open("Primes.txt").read()
for i in sieve.primerange(2,MAXP):
    print(s[p],end="")
    if s[p] == "}":
        print()
        break
    p += i + 1
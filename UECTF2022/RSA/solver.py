from Crypto.Util.number import inverse
from Crypto.Util.number import long_to_bytes

c = 40407051770242960331089168574985439308267920244282326945397
p = 1023912815644413192823405424909
q = 996359224633488278278270361951
e = 65537
n = p*q

d = inverse(e, (p-1)*(q-1))
m = pow(c, d, n)
print(long_to_bytes(m).decode())
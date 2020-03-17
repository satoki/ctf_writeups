from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Util.number import *
import Crypto.PublicKey.RSA as RSA

n = 126390312099294739294606157407778835887
e = 65537
c = 13612260682947644362892911986815626931
p = 9336949138571181619
q = 13536574980062068373
d = inverse(e, (p-1)*(q-1))
key = RSA.construct((n, e, d))
print(long_to_bytes(key.decrypt(c)))
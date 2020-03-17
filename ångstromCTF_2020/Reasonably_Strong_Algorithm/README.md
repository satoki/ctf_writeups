# Reasonably Strong Algorithm:Crypto:70pts
[RSA](rsa.txt) strikes again!  
Hint  
After you get a number, you still have to get a flag from that.  

# Solution
n、e、cが渡されるのでRSAを解読する。  
はじめに(おわりに)msieveを用いて楕円曲線法でnを素因数分解する。  
```text:出力
$ ./msieve -q -v -e 126390312099294739294606157407778835887

~~~
recovered 61 nontrivial dependencies
prp19 factor: 9336949138571181619
prp20 factor: 13536574980062068373
elapsed time 00:00:00
```
以下のプログラムで解いてやる。  
```python:decrypt.py
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
```

## actf{10minutes}
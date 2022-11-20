# RSA:CRYPTO:50pts
RSA暗号でフラグを暗号化してみました！解読してみてください。  
I encrypted the flag with the RSA cipher! Please try to decode it.  

[output.txt](output.txt)　[rsa_source.py](rsa_source.py)  

# Solution
RSAの復号問題。  
output.txtを見ると、pとqが書かれている。  
以下のスクリプトで復号する。  
```python
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
```
実行する。  
```bash
$ python solver.py
UECTF{RSA-iS-VeRy-51Mp1e}
```
flagが得られた。  

## UECTF{RSA-iS-VeRy-51Mp1e}
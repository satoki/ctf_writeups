# STREAMer-Prototype:crypto:100pts
I implemented my prototype STREAM cipher, and I believe it's quite safe. Can you leak my flag from it?  

[Download challenge](f0335659-828f-42b9-857c-390f2e4d5480.zip)  

# Solution
配布された圧縮ファイルには暗号化セットと暗号化したフラグが含まれている。  
暗号化機能を実装したスクリプトの主要部分は以下の通りであった。  
```py
class STREAM:
    def __init__(self, seed, size):
        self.state = self.num2bits(seed, size)

    def num2bits(self, num, size):
        assert num < (1 << size)

        return bin(num)[2:].zfill(size)
    
    def bits2num(self, bits):
        return int('0b' + bits, 2)
    
    def shift(self):
        new_bit = self.state[-1]
        self.state = new_bit + self.state[:-1]

        return new_bit
    
    def getNbits(self, num):
        sequence = ""
        for _ in range(num):
            sequence += self.shift()
        
        return sequence

    def encrypt(self, plaintext):
        ciphertext = b""
        for p in plaintext:
            stream = self.bits2num(self.getNbits(8))
            c = p ^ stream
            ciphertext += bytes([c])

        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = b""
        for c in ciphertext:
            stream = self.bits2num(self.getNbits(8))
            p = c ^ stream
            plaintext += bytes([p])

        return plaintext
~~~
```
XORで暗号化機能が実装されており、復号する関数もあるようだ。  
さらにフラグを以下のスクリプトで暗号化している。  
```py
#!/usr/bin/env python3
from cipher import STREAM
import random


if __name__ == "__main__":
    with open("flag", "rb") as f:
        flag = f.read()

    assert flag[:3] == b'DH{' and flag[-1:] == b'}'

    seed = random.getrandbits(16)
    stream = STREAM(seed, 16)

    print(f"encrypted flag > {stream.encrypt(flag).hex()}")
```
`seed`はランダムな16ビットのようだ。  
総当たりできる範囲なので、以下のborp.pyで行う。  
```py
from cipher import STREAM

with open("output.txt", "r") as f:
    output = f.read()

encflag = bytes.fromhex(output.replace("encrypted flag > ", ""))
for seed in range(0xFFFF):
    stream = STREAM(seed, 16)
    decflag = stream.decrypt(encflag)
    if b"DH{" in decflag:
        print(f"seed = {seed}")
        print(f"flag = {decflag.decode()}")
        break
```
実行する。  
```bash
$ python borp.py
seed = 58654
flag = DH{a2e8d10e942df6ca8851ef12b8b8377d44e8451983958dceaed65adcfb6769ab}
```
flagが得られた。  

## DH{a2e8d10e942df6ca8851ef12b8b8377d44e8451983958dceaed65adcfb6769ab}
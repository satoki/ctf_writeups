# exclusive:Crypto:101pts
XORを使った暗号です🔐  
[encrypt.py](encrypt.py)　　　　[output.txt](output.txt)  

# Solution
encrypt.pyで暗号化したものをoutput.txtに保存したらしい。  
encrypt.pyは以下のようになっている。  
```python:encrypt.py
key = "REDACTED"
flag = "FAKE{this_is_fake_flag}"

assert len(key) == len(flag) == 57
assert flag.startswith("FLAG{") and flag.endswith("}")
assert key[0:3] * 19 == key


def encrypt(s1, s2):
    assert len(s1) == len(s2)

    result = ""
    for c1, c2 in zip(s1, s2):
        result += chr(ord(c1) ^ ord(c2))
    return result


ciphertext = encrypt(flag, key)
print(ciphertext, end="")

```
keyは三文字の連続のようだ。  
XORはもう一度かけると元に戻る性質がある。  
以下のdecrypt.pyで復号する。  
```python:decrypt.py
key = ""
flag = open("output.txt").read()

def encrypt(s1, s2):
    assert len(s1) == len(s2)

    result = ""
    for c1, c2 in zip(s1, s2):
        result += chr(ord(c1) ^ ord(c2))
    return result

for i in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
    for j in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
        for k in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
            key = (i + j + k) * 19
            ciphertext = encrypt(flag, key)
            if "FLAG{" in ciphertext:
                print(ciphertext)
```
実行する。  
```bash
$ python decrypt.py
FLAG{xor_c1ph3r_is_vulnera6le_70_kn0wn_plain7ext_@ttack!}
```
flagが得られた。  

## FLAG{xor_c1ph3r_is_vulnera6le_70_kn0wn_plain7ext_@ttack!}
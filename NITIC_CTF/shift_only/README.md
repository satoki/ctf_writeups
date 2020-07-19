# shift_only:Crypto:200pts
暗号を解読してください！  
[https://www.dropbox.com/s/1h7q3zkapl4x2ry/shift_only.zip?dl=0](shift_only.zip)  

# Solution
解凍するとencrypt_flag.pyとencrypted.flagが出てくる。  
encrypted.flagの中身は以下で、暗号化されたフラグのようだ。  
```text:encrypted.flag
6}bceijnob9h9303h6yg896h0g896h0g896h01b40g896hz
```
encrypt_flag.pyは以下のようになっている。  
```python:encrypt_flag.py
from os import environ
flag = environ["FLAG"]
format = environ["FORMAT"]

shift_table = "abcdefghijklmnopqrstuvwxyz0123456789{}_"
def encrypt(text: str, shift: int) -> str:
    assert  0 <= shift <= 9
    res = ""
    for c in text:
        res += shift_table[(shift_table.index(c)+shift)%len(shift_table)]
    return str(shift) + res
for shift in format:
    flag = encrypt(flag, int(shift))
with open("encrypted.flag", "w") as f:
    f.write(flag)
```
問題文の通り、ただ先頭の数字を使ったシフトをしているだけなようだ。  
ローテーションしているように見える。  
dec_only.pyで戻すとflagになる。  
```python:dec_only.py
shift_table = "abcdefghijklmnopqrstuvwxyz0123456789{}_"
def encrypt(text: str, shift: int) -> str:
    assert  0 <= shift <= 9
    res = ""
    for c in text:
        res += shift_table[(shift_table.index(c)+shift)%len(shift_table)]
    return str(shift) + res

flag = "6}bceijnob9h9303h6yg896h0g896h0g896h01b40g896hz"
while not "nitic_ctf{" in flag:
	flag = encrypt(flag[1:], int(flag[0]))
	print(flag)
```
実行するとflagが得られる。  
```bash
$ python dec_only.py
6ehikoptuhcnc969n_4mbc_n6mbc_n6mbc_n67h{6mbc_n5
6knoquvz0nitic_ctf{shift_shift_shift_and_shift}
```

## nitic_ctf{shift_shift_shift_and_shift}
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
dec_only.pyで戻すとflagになる。  
```python:dec_only.py
shift_table = "abcdefghijklmnopqrstuvwxyz0123456789{}_"
def decrypt(text: str, shift: int) -> str:
    assert  0 <= shift <= 9
    res = ""
    for c in text:
        res += shift_table[(shift_table.index(c)-shift)%len(shift_table)]
    return res

flag = "6}bceijnob9h9303h6yg896h0g896h0g896h01b40g896hz"
while flag[0].isdigit():
	flag = decrypt(flag[1:], int(flag[0]))
	print(flag)
```
実行するとflagが得られる。  
```bash
$ python dec_only.py
589}cdhi83b3xuxb0sa230bua230bua230buv8yua230bt
346{}cd3y9ysps9vn8xyv9p8xyv9p8xyv9pq3tp8xyv9o
1378_a0v6vpmp6sk5uvs6m5uvs6m5uvs6mn0qm5uvs6l
267}_zu5uolo5rj4tur5l4tur5l4tur5lmzpl4tur5k
459{xs3smjm3ph2rsp3j2rsp3j2rsp3jkxnj2rsp3i
156tozoifizldynolzfynolzfynolzfgtjfynolze
45snynhehykcxmnkyexmnkyexmnkyefsiexmnkyd
1ojujdadug}tijguatijguatijguaboeatijgu_
nitic_ctf{shift_shift_shift_and_shift}
```

## nitic_ctf{shift_shift_shift_and_shift}
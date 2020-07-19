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
def encrypt(text: str, shift: int) -> str:
    assert  0 <= shift <= 9
    res = ""
    for c in text:
        res += shift_table[(shift_table.index(c)-shift)%len(shift_table)]
    return str(shift) + res

flag = "6}bceijnob9h9303h6yg896h0g896h0g896h01b40g896hz"
while not "nitic_ctf{" in flag:
	flag = encrypt(flag[1:], int(flag[0]))
	print(flag)
```
実行するとflagが得られる。  
```bash
$ python dec_only.py
6589}cdhi83b3xuxb0sa230bua230bua230buv8yua230bt
6z2359{bc2x8xror8um7wxu8o7wxu8o7wxu8op2so7wxu8n
6twxz3489wr2rlil2og1qro2i1qro2i1qro2ijwmi1qro2h
6nqrtxy23qlwlfcfwiavkliwcvkliwcvkliwcdqgcvkliwb
6hklnrswxkfqf_9_qc7pefcq9pefcq9pefcq9{ka9pefcq8
6befhlmqre_k_636k91j}_9k3j}_9k3j}_9k34e73j}_9k2
68}_bfgkl}6e60x0e3vd563exd563exd563exy}1xd563ew
62568_aef50}0uru}xp{z0x}r{z0x}r{z0x}rs5vr{z0x}q
6wz0267}_zu5uolo5rj4tur5l4tur5l4tur5lmzpl4tur5k
6qtuw0156tozoifizldynolzfynolzfynolzfgtjfynolze
6knoquvz0nitic_ctf{shift_shift_shift_and_shift}
```

## nitic_ctf{shift_shift_shift_and_shift}
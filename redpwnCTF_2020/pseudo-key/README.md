# # <!--XXXXXXXXXX-->
Keys are not always as they seem...  
Note: Make sure to wrap the plaintext with flag{} before you submit!  
[pseudo-key-output.txt](pseudo-key-output.txt)　　　　[pseudo-key.py](pseudo-key.py)  

# Solution
flag{}形式でない文が暗号化されているようだ。  
pseudo-key-output.txtには以下のように暗号文と鍵が書かれている。  
```text:
Ciphertext: z_jjaoo_rljlhr_gauf_twv_shaqzb_ljtyut
Pseudo-key: iigesssaemk
```
pseudo-key.pyは以下のようになっている。  
```python:pseudo-key.py
#!/usr/bin/env python3

from string import ascii_lowercase

chr_to_num = {c: i for i, c in enumerate(ascii_lowercase)}
num_to_chr = {i: c for i, c in enumerate(ascii_lowercase)}

def encrypt(ptxt, key):
    ptxt = ptxt.lower()
    key = ''.join(key[i % len(key)] for i in range(len(ptxt))).lower()
    ctxt = ''
    for i in range(len(ptxt)):
        if ptxt[i] == '_':
            ctxt += '_'
            continue
        x = chr_to_num[ptxt[i]]
        y = chr_to_num[key[i]]
        ctxt += num_to_chr[(x + y) % 26]
    return ctxt

with open('flag.txt') as f, open('key.txt') as k:
    flag = f.read()
    key = k.read()

ptxt = flag[5:-1]

ctxt = encrypt(ptxt,key)
pseudo_key = encrypt(key,key)

print('Ciphertext:',ctxt)
print('Pseudo-key:',pseudo_key)
```
暗号文はもちろんのこと鍵も鍵自身で暗号化されているようだ。  
まずは鍵を探す。  
encrypt関数はそのままにし以下を実行する。  
```python
print(encrypt("abc","abc"))
#ace
print(encrypt("cba","cba"))
#eca
```
位置によらず各桁で暗号化されているようだ。  
以下でアルファベットすべての暗号文を取得できる。  
```python
print(encrypt("abcdefghijklmnopqrstuvwxyz_","abcdefghijklmnopqrstuvwxyz_"))
#acegikmoqsuwyacegikmoqsuwy_
```
鍵はiigesssaemkであり、acegikmoqsuwyが巡回しているので各文字二通りのパターンが考えられる。  
```text
入力:abcdefghijklmnopqrstuvwxyz_
出力:acegikmoqsuwyacegikmoqsuwy_

前半:eedcjjjacgf
後半:rrqpwwwnpts
```
以下のように前後半の鍵で暗号文を総当たりする。  
encrypt関数はそのままにしている。  
```python
flag = ""
c = "z_jjaoo_rljlhr_gauf_twv_shaqzb_ljtyut"
for i in range(len(c)):
    for j in "abcdefghijklmnopqrstuvwxyz_":
        key = "eedcjjjacgf"
        s = encrypt(flag+j, key)
        if s[i] == c[i]:
            flag += j
            break
print(flag)
flag = ""
c = "z_jjaoo_rljlhr_gauf_twv_shaqzb_ljtyut"
for i in range(len(c)):
    for j in "abcdefghijklmnopqrstuvwxyz_":
        key = "rrqpwwwnpts"
        s = encrypt(flag+j, key)
        if s[i] == c[i]:
            flag += j
            break
print(flag)
```
出力は以下となる。  
```text
v_ghrff_pfehdo_xrlf_nrr_pfrhqb_fepurr
i_tuess_csruqb_keys_aee_cseudo_srchee
```
上下のどちらかの文字を選択したものが元の文である。  
i_guess_pseudo_keys_are_pseudo_secureと読める。  
形式を整えるとflagになる。  


## flag{i_guess_pseudo_keys_are_pseudo_secure}
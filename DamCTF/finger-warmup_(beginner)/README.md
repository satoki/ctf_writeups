# finger-warmup (beginner):web:160pts
A finger warmup to prepare for the rest of the CTF, good luck!  
You may find [this](https://realpython.com/python-requests/) or [this](https://programminghistorian.org/en/lessons/intro-to-beautiful-soup) to be helpful.  
[finger-warmup.chals.damctf.xyz](https://finger-warmup.chals.damctf.xyz/)  

# Solution
サイトにアクセスすると以下のようなページだった。  
site  
[site.png](site/site.png)  
```html:index.html
<a href="un5vmavt8u5t5op1u94h">click here, if you are patient enough I will give you the flag</a>
```
クリックするとソースは以下に変化した。  
```html
<a href="bz3nokz7rkmxtef7v5u0v">click here, if you are patient enough I will give you the flag</a>
```
毎回クリックするとhrefが変わるようだ。  
手動でたどるのは難しそうなので以下のhrefhref.pyで行う。  
```python:hrefhref.py
import re
import requests

href = ""
response = ""

try:
    while True:
        url = "https://finger-warmup.chals.damctf.xyz/" + href
        response = requests.get(url)
        nexthref = re.search("<a href=\"(?P<next>.*)\">", response.text)
        href = nexthref.group("next")
        print(href)
        print(response.text)
except:
    print(response.text)
```
実行する。  
```bash
$ python -u hrefhref.py | tee log.txt
un5vmavt8u5t5op1u94h
<a href="un5vmavt8u5t5op1u94h">click here, if you are patient enough I will give you the flag</a>
bz3nokz7rkmxtef7v5u0v
<a href="bz3nokz7rkmxtef7v5u0v">click here, if you are patient enough I will give you the flag</a>
c79rvw7rf823hwad0fle2
<a href="c79rvw7rf823hwad0fle2">click here, if you are patient enough I will give you the flag</a>
2bm1visowi7n5aoll322hs
~~~
<a href="de19g6949wfr4afo7xrqj">click here, if you are patient enough I will give you the flag</a>
24bago4w2bojwtrnotvdik
<a href="24bago4w2bojwtrnotvdik">click here, if you are patient enough I will give you the flag</a>
310491iil95gv69b6qpjp
<a href="310491iil95gv69b6qpjp">click here, if you are patient enough I will give you the flag</a>
Nice clicking, I'm very impressed! Now to go onwards and upwards! <br/><pre>dam{I_hope_you_did_this_manually}</pre>
$ wc -l log.txt
1999 log.txt
```
flagが得られた。  
flag  
[flag.png](site/flag.png)  
1000回ほどクリックすれば手動でも可能だった。  

## dam{I_hope_you_did_this_manually}
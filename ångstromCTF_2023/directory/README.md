# directory:web:40pts
[This](https://directory.web.actf.co/) is one of the directories of all time, and I would definitely rate it out of 10.  

# Solution
リンクが与えられる。  
```bash
$ curl https://directory.web.actf.co/
<html><body><a href="0.html">page 0</a><br />
<a href="1.html">page 1</a><br />
<a href="2.html">page 2</a><br />
~~~
<a href="4998.html">page 4998</a><br />
<a href="4999.html">page 4999</a><br />
</body></html>
$ curl https://directory.web.actf.co/0.html
your flag is in another file
$ curl https://directory.web.actf.co/4999.html
your flag is in another file
```
見ると5000個ものリンクで、内容は当たり以外はすべて同じらしい。  
手動では大変すぎるため、以下のsolver.pyで探索する。  
```python
import sys
import requests

i = 0
while i < 5000:
    try:
        print(i)
        res = requests.get(f"https://directory.web.actf.co/{i}.html").text
        if "your flag is in another file" != res:
            print(res)
            sys.exit(0)
        i += 1
    except Exception as e:
        print(e)
        continue
```
実行する。  
```bash
$ python solver.py
0
1
2
~~~
3053
3054
actf{y0u_f0und_me_b51d0cde76739fa3}
```
3054でflagが得られた。  

## actf{y0u_f0und_me_b51d0cde76739fa3}
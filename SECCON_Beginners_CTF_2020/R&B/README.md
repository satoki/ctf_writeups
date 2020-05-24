# R&B:Crypto:52pts
Do you like rhythm and blues?  
[r_and_b.zip](r_and_b.zip-3c965d79a28098376459eb30aa20fe274e4be833)  

# Solution
解凍するとencoded_flagとproblem.pyが出てくる。  
problem.pyでflagをエンコードしたものがencoded_flagのようだ。  
problem.pyを見ると以下のように記述されている。  
```python:problem.py
~~~
FLAG = getenv("FLAG")
FORMAT = getenv("FORMAT")
~~~
for t in FORMAT:
    if t == "R":
        FLAG = "R" + rot13(FLAG)
    if t == "B":
        FLAG = "B" + base64(FLAG)
~~~
```
FORMATの順でrot13かbase64を行い、先頭にRかBを付与している。  
逆を行えばよい。  
手作業でもできる。  

## ctf4b{rot_base_rot_base_rot_base_base}
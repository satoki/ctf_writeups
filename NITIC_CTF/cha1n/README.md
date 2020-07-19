# cha1n:Misc:200pts
[https://www.dropbox.com/s/4dnnxalaszkvrwj/cha1n.zip?dl=0](cha1n.zip)  

# Solution
cha1n.zipの中に複数のファイルが見られる。  
cha1nの各文字なので、この順につないで実行するとflagが得られる。  
```bash
$ ls
1.bat  1.sh  a.bat  a.sh  c.bat  c.sh  d.bat  h.bat  h.sh  n.bat  n.sh
$ ./c.sh|./h.sh|./a.sh|./1.sh|./n.sh
nitic_ctf{cha1n_cha1n_cha1n_cha1n_cha1n_5combo}
```
Windowsは以下。  
```
> c.bat|h.bat|a.bat|1.bat|n.bat
nitic_ctf{cha1n_cha1n_cha1n_cha1n_cha1n_5combo}
```

## nitic_ctf{cha1n_cha1n_cha1n_cha1n_cha1n_5combo}
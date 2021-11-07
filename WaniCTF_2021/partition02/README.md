# partition02:Forensics:203pts
FLAG01とFLAG02にflag画像を分割して入れておきました．  
添付のファイルは"partition01"と同じものです．  

# Solution
[partition01](../partition01)と同じ添付ファイルを用いるようだ。  
先ほどbinwalkして抽出した中にpngファイルが2つ含まれていた。  
```bash
$ tree _partition.img.extracted/ | grep .png
│   ├── flag01.png
│   ├── flag02.png
```
flag01.pngは途中で切れており、flag02.pngは壊れていた。  
catでファイルを結合する。  
```bash
$ cat flag01.png flag02.png > flag.png
```
![flag.png](flag.png)  
flagが書かれていた。  

## FLAG{you_found_flag_in_FLAGs}
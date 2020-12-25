# let us walk zip:Misc:71pts
あなたはお宝が入っているmain.zipというファイルを入手しました。ただ、なかなか開けられないようです…  
[main.zip](main.zip)  

# Solution
main.zipが配られる。  
問題名からbinwalkのようだ。  
以下のように抽出を行う。  
```bash
$ binwalk -e main.zip

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             gzip compressed data, has original file name: "head.png", from Unix, last modified: 2020-12-19 23:58:53
1613          0x64D           xz compressed data

$ cd _main.zip.extracted/
$ file *
64D:      PNG image data, 500 x 100, 8-bit grayscale, non-interlaced
64D.xz:   XZ compressed data
head.png: PNG image data, 500 x 100, 8-bit grayscale, non-interlaced
```
ファイルが抽出できた。  
![64D](64D)  
![head.png](head.png)  
二つのpngにflagが書かれていた。  

## xm4s{binwalk_is_good_tool}
# Turnips 2:Forensics:150pts
Uh oh.. Parth's file seems to have been corrupted. Can you figure out how to find his flag?  
Hint  
File headers are important, aren't they?  
[file.txt](file.txt)  

# Solution
file.txtが渡されるがどう考えてもtxtではない。  
binwalkしてみる。  
```bash
$ binwalk -e file.txt

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
6284          0x188C          TIFF image data, big-endian, offset of first image directory: 8
6495          0x195F          Unix path: /www.w3.org/1999/02/22-rdf-syntax-ns#">

```
画像のようだが、リネームしても開けない。  
ヘッダーは以下のようになっていた。  
```text
89 6C 76 47 0D 0A 1A 0A 00 00 00 0D 49 39 44 30
```
一般的なpngが壊れているようだ。  
下記に修正する。  
```text
89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52
```
画像が出てきた。  
![file.txt.png](file.txt.png)  
flagが書かれている。  

## nactf{th3_turn1p5_ar3_tak17g_0v35_skf9}
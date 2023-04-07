# 7-Zip:software introduction:50pts
難易度：★☆☆  

> 7-Zipは高圧縮率のファイルアーカイバ(圧縮・展開/圧縮・解凍ソフト)です。  

7-Zipは一般にWindows標準のzip圧縮・展開機能より高機能です。 例えばパスワード付きの圧縮ファイルを作成したり、7z, XZ, BZIP2, GZIP, TAR, ZIP, WIMなど多くのファイル形式の圧縮・展開に対応しています。 以下のページからダウンロードすることができます。 [https://sevenzip.osdn.jp/](https://sevenzip.osdn.jp/)  

[flag.7z](flag.7z)  

# Solution
7zファイルが配られる。  
解凍しても良いが、面倒なのでstringsする。  
```bash
$ strings flag.7z
KogCTF2023{7-Zip_05500900}
```
flagが得られた。  

## KogCTF2023{7-Zip_05500900}
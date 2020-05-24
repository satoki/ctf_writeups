# ws3:Misc:180pts
What the... [record.pcapng](record.pcapng)  
Hint  
Did I send something? Or...  

# Solution
Wiresharkで開く。  
git-upload-packなどの文字が見えるため、gitを扱っていることがすぐにわかる。  
まずは送受信しているファイルを抽出する。  
ws2と同様に「ファイル(F)」->「オブジェクトのエクスポート」->「HTTP...」で18kBのapplication/x-git-receive-packを保存する(git-receive-pack)。  
バイナリエディタなどで開くとgitのpackであることがわかるので、ヘッダー5041434Bの前についているものを消したファイル(git-receive-pack.pack)をunpackする。  
```bash
$ file git-receive-pack.pack
git-receive-pack.pack: Git pack, version 2, 3 objects
$ git init tmp
Initialized empty Git repository in /tmp/.git/
$ cd tmp
tmp$ git unpack-objects < ../git-receive-pack.pack
Unpacking objects: 100% (3/3), done.
tmp$ ls -a
.  ..  .git
```
.git/objectsを見ると、以下の構造になっている。  
```text
objects
├── 34
│   └── b1647544bdcf0e896e080ec84bb8b57cccc8d0
├── 87
│   └── 872f28963e229e8271e0fab6a557a1e5fb5131
├── fe
│   └── 3f47cbcb3ad8e946d0aad59259bdb1bc9e63f2
├── info
└── pack
```
fe/3f47cbcb3ad8e946d0aad59259bdb1bc9e63f2のみファイルサイズが大きいため、これを詳しく見る。  
手始めにzlib_dec.pyでzlib.decompressを行う。  
printするとJFIFと表示されたため、画像ファイルであるようだ。  
zlib_dec.pyをファイルに書き込むよう変更する。  
```python:zlib_dec.py
import zlib

f = open("3f47cbcb3ad8e946d0aad59259bdb1bc9e63f2")
wf = open("image_blob", mode='wb')
wf.write(zlib.decompress(f.read()))
f.close()
wf.close()
```
最後にバイナリエディタなどでヘッダーFFD8の前の部分を削除することにより、画像ファイルとして読み込むことができる。  
画像内にflagが書かれている。  
![image.jpg](image.jpg)  

## actf{git_good_git_wireshark-123323}
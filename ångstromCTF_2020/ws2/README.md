# ws2:Misc:80pts
No ascii, not problem :)  
[recording.pcapng](recording.pcapng)  
Hint  
What did I send?  

# Solution
Wiresharkで開くと画像ファイルをアップロードしていることが分かる。  
「ファイル(F)」->「オブジェクトをエクスポート」->「HTTP...」から102kBあるmultipart/form-dataを保存する(file)。  
これをバイナリエディタで見てみると、jpgヘッダFFD8の前に余計なものがついている。  
これを取ることにより画像として読み込める。  
画像内にflagが書かれている。  
![file.jpg](file.jpg)  

## actf{ok_to_b0r0s-4809813}
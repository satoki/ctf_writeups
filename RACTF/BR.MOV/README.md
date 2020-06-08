# BR.MOV:Misc:400pts
[https://youtu.be/zi3pLOaUUXs](https://youtu.be/zi3pLOaUUXs)  

# Solution
動画を見るとバーコードが映し出され、数字が読まれる。  
[QRコード＆バーコードリーダー](https://play.google.com/store/apps/details?id=com.teacapps.barcodescanner)を使う。  
YouTubeのスロー再生を使うと便利である。  
読まれる数字とバーコードの先頭は一致しているようだ。  
バーコードの中身は以下のようになっていた。  
```text
5WlndrAehA
8PdGSTvnaY
9zuPGubRMc
7cyqggztfa
6AqGoWfWwR
7JwvAOM{Px
4JIEbOEkws
5NDuG4sOeb
9chPBBYtfr
8iwkHVYpcf
7hVMGQe0xL
3vBdLvZLbB
2T3iNatxiU
5kNLb_eoyi
4AfAmLXyJo
4oFE4iSJmP
3ajdUBIXVe
4oAQnoJxEV
8SzMNoIa3j
9aaIBHbqls
2vsDNpidao
1}gfkrtfrm
```
5WlndrAehAではrのように、バーコードの先頭(読まれた数字)のあとからその数字個目を抜き出すとflagになる。  
ractf{b4rc0d3_m4dn3ss}

## ractf{b4rc0d3_m4dn3ss}
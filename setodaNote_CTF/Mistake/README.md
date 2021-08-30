# Mistake:Web:100pts
作成中のサイトに不備があると外部から指摘を受けています。どうやら機密情報が漏れてしまっているようです。サイトにアクセスして機密情報を特定してください。  
以下のサイトにアクセスして隠されたフラグを見つけてください。  
[http://ctf.setodanote.net/web003/](http://ctf.setodanote.net/web003/)  

# Solution
アクセスすると、setodaNote CTFの説明ページのようだ。  
Web - setodaNote CTF  
[site1.png](site/site1.png)  
ソースを見るが何もない。  
試しに画像が配置されているディレクトリ`https://ctf.setodanote.net/web003/images/`を覗くとIndex ofが見られた。  
Index of /images/  
[site2.png](site/site2.png)  
pic_flag_is_here.txtなるファイルがあるので見るとflagが書かれていた。  
```bash
$ curl https://ctf.setodanote.net/web003/images/pic_flag_is_here.txt
flag{You_are_the_Laughing_Man,_aren't_you?}
```

## flag{You_are_the_Laughing_Man,_aren't_you?}
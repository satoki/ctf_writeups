# Welcome to Petstagram:osint:100pts
Who is Alexandros the cat exactly? And who is this mysterious "mum" he keeps talking about?  
Submit his mum's full name in lowercase and with underscores instead of spaces, as the flag: DUCTF{name}  
Hint  
I'm looking for their mum's full name. Are you sure you have everything you need?  
Hint  
If you have Alexandros' mum's given name and surname... what else could there be left to find to get her full name?  

# Solution
mumの名前を探すようだ。  
PetstagramからInstagramを怪しんで検索する。  
Alexandros the catで[alexandrosthecat](https://www.instagram.com/alexandrosthecat/)がヒットした。  
![image1.png](images/image1.png)  
かわいいモノクロの猫とリボンの猫が投稿されている。  
投稿に飼い主(mum)のYouTubeリンクがあった。  
![image2.png](images/image2.png)  
gelato_elgatoというアカウント名だ。  
動画などは投稿されていなかった。  
![image3.png](images/image3.png)  
これをツイッターで検索すると以下の[アカウント](https://twitter.com/gelato_elgato)が出てきた。  
アイコンも猫なので怪しい。  
![image4.png](images/image4.png)  
call me theresaらしい。  
再度Instagramに戻り、alexandrosthecatのフォロワーをサーチすると[emwaters92](https://www.instagram.com/emwaters92/)がヒットした。  
投稿に同じ猫(リボンの猫をモノクロにした写真)が写っている。  
![image5.png](images/image5.png)  
名前がEmily Watersでアカウントがemwaters92なのでEmily T Watersのようだ。  
Tがtheresaである可能性が高い。  
名前を指定されたとおりに整形すると、正しいflagになった。  

## DUCTF{emily_theresa_waters}
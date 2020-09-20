# Welcome to Petstagram:osint:100pts
Who is Alexandros the cat exactly? And who is this mysterious "mum" he keeps talking about?  
Submit his mum's full name in lowercase and with underscores instead of spaces, as the flag: DUCTF{name}  
Hint  
I'm looking for their mum's full name. Are you sure you have everything you need?  
Hint  
If you have Alexandros' mum's given name and surname... what else could there be left to find to get her full name?  

# Solution
PetstagramからInstagramを怪しんで検索する。  
`Alexandros the cat`で[ヒット](https://www.instagram.com/alexandrosthecat/)した。  
![image1.png](images/image1.png)  
投稿に飼い主(mum)のYouTubeリンクがあった。  
![image2.png](images/image2.png)  
gelato_elgatoというアカウント名だ。  
これをツイッターで検索すると以下のアカウントが[出て](https://twitter.com/gelato_elgato)きた。  
![image3.png](images/image3.png)  
call me theresaらしい。  
再度Instagramに戻り、フォロワーをサーチすると``が[ヒット](https://www.instagram.com/emwaters92/)した。  
投稿に同じ猫が写っている。  
![image4.png](images/image4.png)  
名前がEmily Watersでアカウントがemwaters92なのでEmily T Watersのようだ。  
Tがtheresaである可能性が高い。  
flagを指定されたとおりに整形する。  

## DUCTF{emily_theresa_waters}
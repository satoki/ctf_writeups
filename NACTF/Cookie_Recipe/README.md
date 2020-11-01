# Cookie Recipe:Web:150pts
Arjun owns a cookie shop serving warm, delicious, oven-baked cookies. He sent me his ages-old family recipe dating back four generations through this link, but, for some reason, I can't get the recipe. Only cookie lovers are allowed!  
[https://cookies.challenges.nactf.com/index.php](https://cookies.challenges.nactf.com/index.php)  
Hint  
Arjun baked a cookie as an offering, but he accidently placed it on the front page.  

# Solution
URLにアクセスすると以下のページがある。  
Cookie Recipe  
[site1.png](site/site1.png)  
任意の認証情報でログインできるが、レシピは見えないようだ。  
[site2.png](site/site2.png)  
問題URLがindex.phpになっているのが怪しい。  
クッキーを見てみるとuserに`cookie_lover`が入っているが、Pathが`/index.php`になっていた。  
Pathを`/`に直して再度読み込めばよい。  
flag  
[flag.png](site/flag.png)  
flagが得られた。  

## nactf{c00kie_m0nst3r_5bxr16o0z}
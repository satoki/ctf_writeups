# Login:Web:175pts
Vyom has learned his lesson about client side authentication and his soggy croutons will now be protected. There's no way you can log in to this secure portal!  
[https://login.challenges.nactf.com/](https://login.challenges.nactf.com/)  
Hint  
[https://xkcd.com/327/](https://xkcd.com/327/)  

# Solution
URLにアクセスすると以下のようなログインフォームがある。  
Login Page  
[site.png](site/site.png)  
とりあえずSQLインジェクション(`t' OR 't' = 't`)を行う。  
flag  
[flag.png](site/flag.png)  
flagが得られた。  

## nactf{sQllllllll_1m5qpr8x}
# Quarantine:Web:200pts
Challenge instance ready at 95.216.233.106:22888.  
See if you can get access to an account on the webapp.  

# Solution
アクセスするとSign inとSign upがあるが、Sign upは現在停止しているようだ。  
RAQE  
[site.png](../Quarantine_-_Hidden_information/site/site.png)  
Sign inを試みる。  
Login  
[site1.png](site/site1.png)  
Passwordに`'`を入力(Usernameは空)してみると、Internal Server Errorを引き起こせた。  
SQLインジェクションが行えそうだ。  
`t' OR 't' = 't`をPasswordに設定したところ以下のようにAttempting to login as more than one user!??と怒られた。  
Login(more than one user)  
[site2.png](site/site2.png)  
userを制限してやれば良いため、`t' OR LENGTH(username) = 5 --`とする(adminが5文字なのだがユーザはadminではなかったようだ)。  
ログイン成功するとflagがあった。  
flag  
[flag.png](site/flag.png)  

## ractf{Y0u_B3tt3r_N0t_h4v3_us3d_sqlm4p}
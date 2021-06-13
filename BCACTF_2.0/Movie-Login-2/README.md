# Movie-Login-2:webex:150pts
It's that time of year again! Another movie is coming out, and I really want to get some insider information. I heard that you leaked the last movie poster, and I was wondering if you could do it again for me?  
[denylist.json](denylist.json)  
[http://web.bcactf.com:49153/](http://web.bcactf.com:49153/)  
  
Hint 1 of 2  
What steps are they taking to prevent an injection?  
Hint 2 of 2  
Check the denylist maybe?  

# Solution
Movie-Login-1をチームメンバが解いていたためよくわからないがアクセスするとログインフォームのようだ。  
Higher-Tech Login Page  
[site.png](site/site.png)  
テンプレのSQLインジェクションクエリ`' OR 't' = 't' --`を入力すると`Error. SQL Injection detected. Are you breaking in? `と怒られた。  
どうやら配布されたjsonがブラックリストとなっているSQLインジェクション問のようだ。  
denylist.jsonは以下のようであった。  
```json:denylist.json
[
    "1",
    "0",
    "/",
    "="
]
```
`=`が引っかかっているようなので`' OR true --`とすればよい。  
[flag.png](site/flag.png)  
ログインに成功し、flagが得られた。  

## bcactf{h0w_d1d_y0u_g3t_h3r3_th1s_t1m3?!?}
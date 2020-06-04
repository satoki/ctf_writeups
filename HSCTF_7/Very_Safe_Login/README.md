# Very Safe Login:Web Exploitation:100pts
Bet you can't log in.  
[https://very-safe-login.web.hsctf.com/very-safe-login](https://very-safe-login.web.hsctf.com/very-safe-login)  

# Solution
ただのログインフォームのようだ。  
Login  
[site.png](site/site.png)  
ソースに以下を見つけることができる。  
```JavaScript
~~~
            const username = login.username.value;
            const password = login.password.value;
            
            if(username === "jiminy_cricket" && password === "mushu500") {
                showFlag();
                return false;
            }
~~~
```
jiminy_cricketになればよい。  
flag  
[flag.png](site/flag.png)  

## flag{cl13nt_51de_5uck5_135313531}
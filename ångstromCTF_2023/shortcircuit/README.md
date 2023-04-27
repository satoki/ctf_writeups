# shortcircuit:web:40pts
[Bzzt](https://shortcircuit.web.actf.co/)  

# Solution
リンクが渡されるので、アクセスするとログインフォームのようだ。  
![site.png](site/site.png)  
ソースを見ると以下のようであった。  
```html
<html>
    <head>
        <title>Short Circuit</title>

        <script>
            const swap = (x) => {
                let t = x[0]
                x[0] = x[3]
                x[3] = t

                t = x[2]
                x[2] = x[1]
                x[1] = t

                t = x[1]
                x[1] = x[3]
                x[3] = t

                t = x[3]
                x[3] = x[2]
                x[2] = t

                return x
            }

            const chunk = (x, n) => {
                let ret = []

                for(let i = 0; i < x.length; i+=n){
                    ret.push(x.substring(i,i+n))
                }

                return ret
            }

            const check = (e) => {
                if (document.forms[0].username.value === "admin"){
                    if(swap(chunk(document.forms[0].password.value, 30)).join("") == "7e08250c4aaa9ed206fd7c9e398e2}actf{cl1ent_s1de_sucks_544e67ef12024523398ee02fe7517fffa92516317199e454f4d2bdb04d9e419ccc7"){
                        location.href="/win.html"
                    }
                    else{
                        document.getElementById("msg").style.display = "block"
                    }
                }
            }
        </script>
    </head>
    <body>
        <form>
            <input name="username" placeholder="Username" type="text" />
            <input name="password" placeholder="Password" type="password" />

            <input type="button" onclick="check()" value="Log in"/>
        </form>
        <p id="msg" style="display:none;color:red;">Username or password incorrect</p>
    </body>
</html>
```
入力を`chunk`して`swap`したのちにフラグであったようなものと比較している。  
動作として30文字ずつに分割し、入れ替えているようだ。  
これを戻せば良い。  
```js
$ node
> const new_swap = (x) => {
...     let t = x[3]
...     x[3] = x[2]
...     x[2] = t
...
...     t = x[1]
...     x[1] = x[3]
...     x[3] = t
...
...     t = x[2]
...     x[2] = x[1]
...     x[1] = t
...
...     t = x[0]
...     x[0] = x[3]
...     x[3] = t
...
...     return x
... }
> const chunk = (x, n) => {
...     let ret = []
...
...     for(let i = 0; i < x.length; i+=n){
...         ret.push(x.substring(i,i+n))
...     }
...
...     return ret
... }
> new_swap(chunk("7e08250c4aaa9ed206fd7c9e398e2}actf{cl1ent_s1de_sucks_544e67ef12024523398ee02fe7517fffa92516317199e454f4d2bdb04d9e419ccc7", 30)).join("")
'actf{cl1ent_s1de_sucks_544e67e6317199e454f4d2bdb04d9e419ccc7f12024523398ee02fe7517fffa92517e08250c4aaa9ed206fd7c9e398e2}'
```
flagが復元できた(ちなみにログインしても何もない)。  

## actf{cl1ent_s1de_sucks_544e67e6317199e454f4d2bdb04d9e419ccc7f12024523398ee02fe7517fffa92517e08250c4aaa9ed206fd7c9e398e2}
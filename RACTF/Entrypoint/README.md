# Entrypoint:Web:200pts
Challenge instance ready at 95.216.233.106:31789.  
Sadly it looks like there wasn't much to see in the python source. We suspect we may be able to login to the site using backup credentials, but we're not sure where they might be. Encase the password you find in ractf{...} to get the flag.  
This challenge does NOT have fake flags. If you found some other flags while solving this challenge, you may have found the solutions to the next challenges first :P  

# Solution
アクセスするとログインフォームが見える。  
Login  
[site.png](site/site.png)  
まずはソースを確認すると、以下のような記述があった。  
```html
~~~
        <link href="https://fonts.googleapis.com/css?family=Nanum+Gothic:400,700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="/static?f=index.css">

        <title>Login</title>
~~~
            <!--
                In case I forget: Backup password is at ./backup.txt
            -->
~~~
```
/static?f=でbackup.txtを読み込むと問題の意味に沿う。  
http://95.216.233.106:31789/static?f=backup.txt には以下が書かれていたのでflag形式にする。  
```text:backup.txt
develop    developerBackupCode4321

Make sure to log out after using!

TODO: Setup a new password manager for this
```
ractf{developerBackupCode4321}がflag。  

## ractf{developerBackupCode4321}
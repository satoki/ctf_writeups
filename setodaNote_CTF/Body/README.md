# Body:Web:30pts
作成中のサイトに機密情報が含まれてしまっているようです。サイトにアクセスして機密情報を見つけ出してください。  
以下のサイトにアクセスして隠されたフラグを見つけてください。  
[https://ctf.setodanote.net/web001/](https://ctf.setodanote.net/web001/)  

# Solution
問題名の通りbodyを見てみる。  
```bash
$ curl https://ctf.setodanote.net/web001/ | grep flag{
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  6859    0  6859    0     0  42079      0 --:--:-- --:--:-- --:--:-- 42079
                                                        <p>特に指定がない限りフラグは flag{<!-- *** flag{Section_9} *** -->} という形式をとります。</p>
```
コメントでflagが書かれていた。  

## flag{Section_9}
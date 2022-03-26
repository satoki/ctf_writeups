# Logs:Web:200pts
Our apache server is under attack. Thoses are the access logs of the server, can you find out what they are doing?  
![Apache_server.png](images/Apache_server.png)  
Notre serveur apache est sous attaque. Voici les journaux d'accès du serveur, pouvez-vous savoir ce qui se passe ?  
ZIP PASSWORD: 0FPP7C7F  
Hint  
I you scroll the log file text, you will find lines containing suspicious requests.  
Hint  
Decode the suspicious requests found  
[access.log.zip](access.log.zip)  

# Solution
zipファイルが配布されるので指定された`0FPP7C7F`で解凍する。  
中身を確認するとapacheのアクセスログファイルのようだ。
```
$ head -n 5 access.log.ctf
find the flag! khkhkh
192.168.32.1 - - [29/Sep/2015:03:28:43 -0400] "GET /dvwa/robots.txt HTTP/1.1" 200 384 "-" "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
192.168.32.1 - - [29/Sep/2015:03:28:43 -0400] "GET /favicon.ico HTTP/1.1" 404 503 "http://192.168.32.134/dvwa/robots.txt" "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
192.168.32.1 - - [29/Sep/2015:03:28:48 -0400] "GET /dvwa/robots.txt HTTP/1.1" 304 209 "-" "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
192.168.32.1 - - [29/Sep/2015:03:28:51 -0400] "GET /dvwa HTTP/1.1" 301 557 "-" "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
```
フラグが中に入っているようなので、眺めているとSQLiの試行ログが目に入った。  
```
192.168.32.1 - - [29/Sep/2015:03:37:34 -0400] "GET /mutillidae/index.php?page=user-info.php&username=%27+union+all+select+1%2CString.fromCharCode%2870%2c+76%2c+65%2c+71%2c+32%2c+73%2c+83%2c+32%2c+58%2c+32%2c+79%2c+70%2c+80%2c+80%2c+84%2c+45%2c+67%2c+84%2c+70%2c+123%2c+76%2c+48%2c+103%2c+115%2c+95%2c+114%2c+50%2c+118%2c+51%2c+52%2c+108%2c+51%2c+100%2c+95%2c+83%2c+81%2c+76%2c+95%2c+49%2c+110%2c+106%2c+51%2c+99%2c+116%2c+49%2c+48%2c+110%2c+125%29%2C3+--%2B&password=&user-info-php-submit-button=View+Account+Details HTTP/1.1" 200 9582 "http://192.168.32.134/mutillidae/index.php?page=user-info.php&username=something&password=&user-info-php-submit-button=View+Account+Details" "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
```
デコードすると以下になる。  
```
192.168.32.1 - - [29/Sep/2015:03:37:34 -0400] "GET /mutillidae/index.php?page=user-info.php&username=' union all select 1,String.fromCharCode(70, 76, 65, 71, 32, 73, 83, 32, 58, 32, 79, 70, 80, 80, 84, 45, 67, 84, 70, 123, 76, 48, 103, 115, 95, 114, 50, 118, 51, 52, 108, 51, 100, 95, 83, 81, 76, 95, 49, 110, 106, 51, 99, 116, 49, 48, 110, 125),3 --+&password=&user-info-php-submit-button=View Account Details HTTP/1.1" 200 9582 "http://192.168.32.134/mutillidae/index.php?page=user-info.php&username=something&password=&user-info-php-submit-button=View Account Details" "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
```
`70,76,65,71`始まりなので、`FLAG`から始まっていそうだ。  
pythonで文字に起こしてみる。  
```bash
$ python
~~~
>>> text = [70, 76, 65, 71, 32, 73, 83, 32, 58, 32, 79, 70, 80, 80, 84, 45, 67, 84, 70, 123, 76, 48, 103, 115, 95, 114, 50, 118, 51, 52, 108, 51, 100, 95, 83, 81, 76, 95, 49, 110, 106, 51, 99, 116, 49, 48, 110, 125]
>>> for c in text:
...     print(chr(c), end="")
...
FLAG IS : OFPPT-CTF{L0gs_r2v34l3d_SQL_1nj3ct10n}>>>
```
flagが得られた。  

## OFPPT-CTF{L0gs_r2v34l3d_SQL_1nj3ct10n}
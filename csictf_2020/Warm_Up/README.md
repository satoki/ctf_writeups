# Warm Up:Web:XXXpts<!--XXX-->
If you know, you know; otherwise you might waste a lot of time.  
[http://chall.csivit.com:30272](http://chall.csivit.com:30272/)  

# Solution
アクセスすると以下のphpのソースが出てくる。  
```php
<?php

if (isset($_GET['hash'])) {
    if ($_GET['hash'] === "10932435112") {
        die('Not so easy mate.');
    }

    $hash = sha1($_GET['hash']);
    $target = sha1(10932435112);
    if($hash == $target) {
        include('flag.php');
        print $flag;
    } else {
        print "csictf{loser}";
    }
} else {
    show_source(__FILE__);
}

?>
```
hashクエリのsha1を衝突させるとflagが出るようだ。  
しかし文字が異なる必要があるため現実的ではない。  
ここで以下に注目する。  
```php
~~~
    $hash = sha1($_GET['hash']);
    $target = sha1(10932435112);
    if($hash == $target) {
~~~
```
厳密等価演算子ではないのでphpはキャストして比較してしまう。  
以下のようにsha1が`0e07766915004133176347055865026311692244`になるので、数値`0`と等価だと判定されるらしい。  
```bash
$ php -a
~~~
php > print (sha1(10932435112));
0e07766915004133176347055865026311692244
```
`0e`から始まる文字列を探してやればいい。  
以下が知られている。  
```text
aaroZmOk    0e66507019969427134894567494305185566735
aaK1STfY    0e76658526655756207688271159624026011393
aaO8zKZF    0e89257456677279068558073954252716165668
aa3OFF9m    0e36977786278517984959260394024281014729
```
どれでもいいが、ここでは?hash=aaroZmOkでアクセスする。  
するとflagが表示された。  
flag  
[flag.png](site/flag.png)  

## csictf{typ3_juggl1ng_1n_php}
# php:Web:481pts
This website is broken; it shows its php source code. Can you find a way to read the flag.  
No scanners needed for this challenge!  
![php.png](images/php.png)  
Ce site Web affiche son code source php. Pouvez-vous trouver un moyen de lire le flag.  
N'utilisez pas des outils de scan pour ce défi !  
[http://143.198.224.219:20000](http://143.198.224.219:20000/)  

# Solution
URLが渡されるのでアクセスしてみる。  
[site1.png](site/site1.png)  
以下のコードが表示されていた。  
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
        print "OFPPT-CTF{not-the-one}";
    }
} else {
    show_source(__FILE__);
}

?>
```
クエリパラメータからの入力と`10932435112`のハッシュが同一であればフラグが得られる。  
`10932435112`はCTFではよく見る、ハッシュ後の文字列がphpの比較により数字と解釈されてしまうものだ。  
同様の文字列として`aaroZmOk`も知られている。  
`http://143.198.224.219:20000/?hash=aaroZmOk`にアクセスすればよい。  
[flag.png](site/flag.png)  
flagが表示された。  

## OFPPT-CTF{typ3_juggl1ng_1n_php}
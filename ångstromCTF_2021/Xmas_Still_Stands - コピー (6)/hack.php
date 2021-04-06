<?php
$URI = $_SERVER['REQUEST_URI'];
echo $URI;
$fp = fopen("hack.txt", "w");
fwrite($fp, $URI);
fclose($fp);
?>
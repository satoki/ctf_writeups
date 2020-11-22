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
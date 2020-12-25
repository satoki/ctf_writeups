<?php

$content = "";
if (isset($_GET["ext"])) {
	$content = file_get_contents("resource/" . $_GET["ext"]);
}

?>

<!DOCTYPE html>
<html lang="ja">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>HelloWorld</title>
	<style type="text/css">
		pre {
		  margin: 1em 0;
		  padding: 1em;
		  background: #25292f;
		  color: #fff;
		  white-space: pre-wrap;
		}
	</style>
</head>
<body>
	<h1>Hello World!</h1>
	<form>
		<select name="ext">
			<option value="hello.js">JavaScript</option>
			<option value="hello.py">Python</option>
			<option value="hello.rs">Rust</option>
			<option value="hello.c">C</option>
		</select>
		<input type="submit" value="View">
	</form>
	<pre><?php echo htmlspecialchars($content, ENT_QUOTES) ?></pre>
</body>
</html>

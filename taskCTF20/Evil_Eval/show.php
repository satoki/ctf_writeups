<?php
$result = "";
    if (isset($_GET['data'])) {
        $data = $_GET['data'];
        $raw = base64_decode($data);
        eval('$result = ' . $raw . ';');
    }
?>
<html>
<head>
    <meta charset="utf-8">
    <title>result</title>
</head>
<body>
    <h1>結果</h1>
    <p><?= $result ?></p>
</body>
</html>
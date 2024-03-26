# WebDecode:Web Exploitation:50pts
Do you know how to use the web inspector?  
Start searching [here](http://titan.picoctf.net:60527/) to find the flag  

Hints  
1  
Use the web inspector on other files included by the web page.  
2  
The flag may or may not be encoded  

# Solution
URLが渡される。  
アクセスすると、以下のようなホームページであった。  
![site.png](site/site.png)  
ソースは以下の通りであった。  
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="style.css">
  <link rel="shortcut icon" href="img/favicon.png" type="image/x-icon">
  <!-- font (google) -->
  <link href="https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
  <title>Home</title>
</head>
<body>
<header>
  <nav>
    <div class="logo-container">
      <a href="index.html"><img src="img/binding_dark.gif" alt="logo"></a>
    </div>
    <div class="navigation-container">
      <ul>
        <li><a href="index.html">Home</a></li>
        <li><a href="about.html">About</a></li>
        <li><a href="contact.html">Contact</a></li>
      </ul>
    </div>
  </nav>
</header>
  <section class="banner">
    <h1>Ha!!!!!! You looking for a flag?</h1>
    <p>Keep Navigating</p>
  
  </section><!-- .banner -->
  <section class="sec-intro">
    <div class="col">
      <p>Haaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa</p>
      <p>Keepppppppppppppp Searchinggggggggggggggggggg</p>
      <img src="./img/multipage-html-img1.jpg" alt="person">
      <figcaption>Don't give up!</figcaption>
    </div>
  </section><!-- .sec-intro -->
  
  <footer>
    <div class="bottombar">Copyright © 2023 Your_Name. All rights reserved.</div>
  </footer>
  
</body>
</html>
```
flagがどこかに隠れているらしい。  
探すのが面倒なのでひとまずgrepする。  
```bash
$ curl -s http://titan.picoctf.net:60527/{index.html,about.html,contact.html} | grep picoCTF
$ curl -s http://titan.picoctf.net:60527/{index.html,about.html,contact.html} | grep cGljb
  <section class="about" notify_true="cGljb0NURnt3ZWJfc3VjYzNzc2Z1bGx5X2QzYzBkZWRfMTBmOTM3NmZ9">
$ echo -n 'cGljb0NURnt3ZWJfc3VjYzNzc2Z1bGx5X2QzYzBkZWRfMTBmOTM3NmZ9' | base64 -d
picoCTF{web_succ3ssfully_d3c0ded_10f9376f}
```
base64したものでヒットし、デコードするとflagとなった。  

## picoCTF{web_succ3ssfully_d3c0ded_10f9376f}
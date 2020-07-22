# Cascade:Web:100pts
Welcome to csictf.  
[http://chall.csivit.com:30203](http://chall.csivit.com:30203/)  

# Solution
URLにアクセスすると紫色のページに飛ぶ。  
Cascade  
[site.png](site/site.png)  
ソースを見るとcssがあるようなので開くと以下のようになっている。  
```css:style.css
body {
    background-color: purple;
    text-align: center;
    display: flex;
    align-items: center;
    flex-direction: column;
}

h1, div, a {
    /* csictf{w3lc0me_t0_csictf} */
    color: white;
    font-size: 3rem;
}
```
flagが書かれている。

## csictf{w3lc0me_t0_csictf}
# Ador:Web Exploitation:50pts
Ada was born on 10 December 1815 not 12, identification change makes a difference  
Link: [http://104.198.67.251/Ador](http://104.198.67.251/Ador)  

# Solution
URLにアクセスすると謎のサイトが出てくる。  
3 Column Layout  
[site.png](site/site.png)  
リロードごとに文章が変化しているようだ。  
"Welcome user, secrets only for admin"と言われている。  
ソースの以下に注目する。  
```html
~~~
<body>
<!-- try the parameter `name` user -->

        <header id="header"><p>Header...</p></header>
~~~
```
nameを指定しろということだろうか。  
`http://104.198.67.251/Ador/?name=admin`にアクセスするとflagが表示された。  
flag  
[flag.png](site/flag.png)  

## shaktictf{f1r5t_c0mpu73r_pr0gr4mm3r}
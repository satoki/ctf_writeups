# Inspect:Web:50pts
Lola's new to website-building. Having just learned HTML and CSS, she built this site and embedded some dark secrets. I wonder where I could find them.  
[http:/inspect.challenges.nactf.com/](http://inspect.challenges.nactf.com/)  

# Solution
URLにアクセスするとのようなサイトがあった。  
I wonder what Inspect means?  
[site1.png](site/site1.png)  
[site2.png](site/site2.png)  
HTMLとCSSが選択できる。  
ソースを見るとstyle.cssがあるようだ。  
```css
~~~
.tabcontent {
    padding: 50px;
    text-align: center;
    font-size: 20px;
}

/*Inspecting other people's code is a good way to learn. nactf{1nspect1ng_sp13s_4_lyf3} */
```
flagが書かれていた。  

## nactf{1nspect1ng_sp13s_4_lyf3}
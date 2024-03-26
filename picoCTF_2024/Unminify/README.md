# Unminify:Web Exploitation:100pts
I don't like scrolling down to read the code of my website, so I've squished it. As a bonus, my pages load faster!  
Browse [here](http://titan.picoctf.net:53048/), and find the flag!  

Hints  
1  
Try CTRL+U / ⌘+U in your browser to view the page source. You can also add 'view-source:' before the URL, or try `curl <URL>` in your shell.  
2  
Minification reduces the size of code, but does not change its functionality.  
3  
What tools do developers use when working on a website? Many text editors and browsers include formatting.  

# Solution
URLが渡される。  
アクセスすると以下のようなサイトであった。  
![site.png](site/site.png)  
ソースを見るとminifyされており、問題名の通りほどいてフラグを探すようだ。  
```bash
$ curl -s 'http://titan.picoctf.net:53048/' | grep -Po 'picoCTF{.*?}'
picoCTF{pr3tty_c0d3_ed938a7e}
```
grepすると見つかった。  

## picoCTF{pr3tty_c0d3_ed938a7e}
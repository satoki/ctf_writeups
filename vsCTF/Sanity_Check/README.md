# Sanity Check:Web:100pts
[https://challs.viewsource.me/sanity-check](https://challs.viewsource.me/sanity-check/)  

# Solution
URLが渡されるのでアクセスすると謎のサイトであった。  
Sanity Check  
[site.png](site/site.png)  
静的なサイトなので、ソースを見てみる。  
```bash
$ curl https://challs.viewsource.me/sanity-check/
~~~
  <body>
    <div class="centered">
      <h1>What does <vs>VS</vs> stand for in <vs>&lt;vsCTF/&gt;</vs>?</h1>
      <!-- vsctf{v1ew_s0urc3_a_f1rst_y3ar_t3am!} -->
    </div>
  </body>
</html>
```
flagが書かれていた。  

## vsctf{v1ew_s0urc3_a_f1rst_y3ar_t3am!}
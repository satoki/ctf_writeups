# Blurry Eyes:Web Exploitation:100pts
I can't see :(  
[https://blurry-eyes.web.hsctf.com](https://blurry-eyes.web.hsctf.com)  

# Solution
アクセスするとCTFについての解説サイトのようだ。  
Blurry Eyes  
[site.png](site/site.png)  
ページ終わりにあるブラーがかかっている部分が怪しい。  
ソースを見ると以下のようになっている。  
```html
~~~
    <h4>Anyways, the flag that you need for this cha<span class="blur">llenge is: <span
          class="poefKuKjNPojzLDf"></span></span></h4>
~~~
```
この`<span class="blur">`を開発者ツールなどで`<span class="">`へ変更してやるとflagが得られる。  
flag  
[flag.png](site/flag.png)  
別解としては、poefKuKjNPojzLDfをstyle.cssから探す方法もある。  
```css
~~~
.poefKuKjNPojzLDf:after {
	content: "f" "l" "a" "g" "{" "g" "l" "a" "s" "s" "e" "s" "_" "a" "r" "e" "_" "u" "s" "e" "f" "u" "l" "}" ;
}
~~~
```

## flag{glasses_are_useful}
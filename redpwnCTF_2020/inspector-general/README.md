# inspector-general:web:112pts
My friend made a new webpage, can you [find a flag?](https://redpwn.net/)  

# Solution
アクセスするとWriteupが置いてあるサイトに飛ぶ  
Home  
[site.png](site/site.png)  
ソースコードを見ると以下の記述があった。  
```html
~~~
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="redpwnctf2020" content="flag{1nspector_g3n3ral_at_w0rk}">
    <title>Home | redpwn</title>
~~~
```
metaタグ内にflagがある。  

## flag{1nspector_g3n3ral_at_w0rk}
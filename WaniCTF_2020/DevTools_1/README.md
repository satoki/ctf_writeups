# DevTools_1:Web:pts
ブラウザの開発者ツールを使ってソースコードをのぞいてみましょう！  
[https://devtools1.wanictf.org](https://devtools1.wanictf.org/)  

# Solution
ソースコードに隠されているようなのでcurlしてgrepする。  
```bash
$ curl -s https://devtools1.wanictf.org/ | grep FLAG
    <!-- FLAG{you_can_read_html_using_devtools} -->
```
flagがコメントアウトされていた。  

## FLAG{you_can_read_html_using_devtools}
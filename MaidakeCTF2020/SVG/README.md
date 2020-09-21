# SVG:Misc:100pts
これはただの画像ではありません。 [https://aokakes.work/MaidakeCTF2020/SVG/](https://aokakes.work/MaidakeCTF2020/SVG/)  
Hint  
SVGの中身を見ましょう  

# Solution
URLにアクセスすると以下のようなサイトだった。  
SVG  
[site.png](site/site.png)  
svgのみが置かれている。  
![flag.svg](flag.svg)  
中身が怪しそうなのでsvgをwgetし、stringsしてgrepする。  
```bash
$ wget https://aokakes.work/MaidakeCTF2020/SVG/flag.svg
~~~
$ strings flag.svg | grep MaidakeCTF{
   flag="MaidakeCTF{SVG_images_are_composed_of_XML}">
```
flagが書かれていた。  

## MaidakeCTF{SVG_images_are_composed_of_XML}
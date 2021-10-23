# JELLY FISH:FORENSICS:100pts
この写真を撮影したスマートフォンが起動した時間を示せ。(日本時間）  
What is the boot time of the smartphone that took this picture? (Answer in JST)  
  
**フラグ形式 / FlagFormat**  
`yyyy/mm/dd hh:mm:ss`  
[IMG_2650.HEIC](IMG_2650.HEIC)  

# Solution
exifを見てやると何かわかりそうなので、exiftoolに食わせる。  
```bash
$ exiftool IMG_2650.HEIC
~~~
Run Time Since Power Up         : 4 days 1:49:02
Aperture                        : 1.8
Image Size                      : 4032x3024
Megapixels                      : 12.2
Scale Factor To 35 mm Equivalent: 6.1
Shutter Speed                   : 1/30
Create Date                     : 2021:10:02 13:41:09.853+09:00
Date/Time Original              : 2021:10:02 13:41:09.853+09:00
Modify Date                     : 2021:10:02 13:41:09+09:00
~~~
```
`Run Time Since Power Up`がわかるようなので、それを撮影時間から引けばよい。  
```
Run Time Since Power Up         : 4 days 1:49:02
Create Date                     : 2021:10:02 13:41:09.853+09:00
```
日本時間を計算し、指定されたとおりに整形すると`2021/09/28 11:52:07`となる。  
これがflagだった。  

## 2021/09/28 11:52:07
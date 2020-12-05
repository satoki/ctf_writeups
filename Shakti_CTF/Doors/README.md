# Doors:Web Exploitation:100pts
Ada Loves to travel to places, London-Paris-Spain and discover more  
Link: [http://35.225.9.113/Doors/](http://35.225.9.113/Doors/)  

# Solution
URLにアクセスすると複数のphpページへのエントランスが表示される。  
Explore Dora!!  
[site1.png](site/site1.png)  
ソースの以下の部分に注目する。  
```html
~~~
		[<em><a href="file1.php">file1.php</a></em>] - [<em><a href="file2.php">file2.php</a></em>] - [<em><a href="file3.php">file3.php</a></em>]
	</div></h3>

			</div>
<!-- ?page -->
			<div class="clear">
			</div>
~~~
```
`?page`なるコメントがなされている。  
index.phpを指定した`http://35.225.9.113/Doors/?page=index.php`にアクセスしてみる。  
?page=index.php  
[site5.png](site/site5.png)  
ファイルが読み込めている。  
ディレクトリトラバーサルに狙いをつけて、`/etc/passwd`を取得してみる。  
`http://35.225.9.113/Doors/?page=/etc/passwd`にアクセスするとflagが表示された。  
flag  
[flag.png](site/flag.png)  

## shaktictf{c4lculu5_0f_7h3_n3rv0u5_5y5t3m}
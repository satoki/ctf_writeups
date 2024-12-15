# Toolong Tea:web:100pts
Recently it's getting colder in Tokyo which TSG is based in. Would you like to have a cup of hot oolong tea? It will warm up your body.  

### Hint for beginners  
- First of all, please open the given website and play around with it. This challenge claims that you can get the flag by sending the number `65536` to the server, but it quickly turns out that the story isn't that simple.  
- Next, please read the attached source code. The file `server.js` contains the important logic of this website. The flag is stored in a variable called `flag`, so the purpose is to leak this value.  
- There is a bug which can be exploited to get the flag. Some knowledge of web technologies, especially JavaScript, may be required, so please refer to documentation such as MDN if necessary.  
- You can run this website locally as usual Node.js app (`npm install && node server.js`), or via docker compose (`docker compose up --build`).  
- Note that you do not need a large volume of accesses to solve this problem. Please refrain from mass access similar to DoS.  

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
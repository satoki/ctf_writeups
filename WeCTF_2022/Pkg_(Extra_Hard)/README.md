# Pkg (Extra Hard):Web:846pts
Shou hoards the flag better with more obfuscation now. He looks scared.  
Hint: How about capturing what is sent to remote server?  
[Source Code](pkg2.zip)  

# Solution
[Pkg](../Pkg)の強化問題のようだ。  
ひとまず実行すると`App listening on port 10001`と同じく10001番でサーバが立ち上がる。  
アクセスすると以下のようなページであった。  
![image1.png](images/image1.png)  
猫ちゃん(さん？)が謎のコインを押している。  
`twnxtodoqaixrmbwytpqeerfraxpjz`との文字列が見えるが、暗号文にしては短い。  
Pkgと同じくエントリーポイントを書き換えるためにgrepする。  
```bash
$ strings binaryexpress2-win.exe | grep snapshot
~~~
{"C:\\snapshot\\binaryExpress\\flag2\\server.js":{"0":[0,3840],"3":[3840,120]},"C:\\snapshot\\binaryExpress\\flag2\\package.json":{"1":[3960,457],"3":[4417,119]},"C:\\snapshot\\binaryExpress\\flag2\\views\\flag.ejs":{"1":[4536,24092],"3":[28628,121]},"C:\\snapshot\\binaryExpress\\flag2\\jwtRS256.key":{"1":[28749,3243],"3":[31992,120]},"C:\\snapshot\\binaryExpress\\flag2\\node_modules\\axios\\package.json":{"1":[32112,2429],"3":[34541,120]},"C:\\snapshot\\binaryExpress\\flag2\\node_modules\\axios\\index.js":{"0":[34661,584],"1":[35245,40],"3":[35285,118]},"C:\\snapshot\\binaryExpress\\flag2\\node_modules\\ejs\\package.json":{"1":[35403,896],"3":[36299,119]},"C:\\snapshot\\binaryExpress\\flag2\\node_modules\\ejs\\lib\\ejs.js":{"0":[36418,20920],"1":[57338,27481],"3":[84819,121]},"C:\\snapshot\\binaryExpress\\flag2\\node_modules\\express\\package.json":{"1":[84940,2623],"3":[87563,120]},"C:\\snapshot\\binaryExpress\\flag2\\node_modules\\express\\index.js":{"0":[87683,584],"1":[88267,224],"3":[88491,119]},"C:\\snapshot\\binaryExpress\\flag2\\encryption1.js":{"0":[88610,1488],"3":[90098,119]},"C:\\snapshot\\binaryExpress\\node_modules\\jsonwebtoken\\package.json":{"1":[90217,1511],"3":[91728,120]},"C:\\snapshot\\binaryExpress\\node_modules\\jsonwebtoken\\index.js":{"0":[91848,1024],"1":[92872,276],"3":[93148,119]},"C:\\snapshot\\binaryExpress\\flag2"
~~~
"C:\\snapshot\\binaryExpress\\flag2\\node_modules\\color-name":{"2":[3401220,27],"3":[3401247,117]},"C:\\snapshot\\binaryExpress\\flag2\\node_modules\\filelist\\node_modules":{"2":[3401364,31],"3":[3401395,117]},"C:\\snapshot\\binaryExpress\\flag2\\node_modules\\iconv-lite\\encodings\\tables":{"2":[3401512,126],"3":[3401638,117]}}
"C:\\snapshot\\binaryExpress\\flag2\\server.js"
```
こちらも同様に`C:\\snapshot\\binaryExpress\\flag2\\server.js`の`C:\\snapshot`を`C:\\snapshoo`とし、ローカルの`C:\snapshoo\binaryExpress\flag2\server.js`を実行する。  
まず初めに望みは薄いが、`C:\snapshot\binaryExpress\flag2\server.js`の取得を試みる。  
```js
const fs = require("fs");
var data = fs.readFileSync("C:\\snapshot\\binaryExpress\\flag2\\server.js").toString("utf8");
console.log(data);
```
```
>binaryexpress2-win_snapshoo.exe
source-code-not-available
```
やはり駄目なようだ。  
次に重要そうである`C:\snapshot\binaryExpress\flag2\jwtRS256.key`を取得する。  
```js
const fs = require("fs");
//var data = fs.readFileSync("C:\\snapshot\\binaryExpress\\flag2\\server.js").toString("utf8");
var data = fs.readFileSync("C:\\snapshot\\binaryExpress\\flag2\\jwtRS256.key").toString("hex");
console.log(data);
```
```
>binaryexpress2-win_snapshoo.exe
2d2d2d2d2d424547494e205253412050524956415445204b45592d2d2d2d2d0a4d49494a4b41494241414b43416745416c3569334775486a6d4c3065784b4448776f4a3862452f4659414155642f79725056542b4e422f7144487836486d43530a68493230415a446c746354415963456b646e56506a716347512f4779467059796a774f614d554a36527a6e77386433734278554e74564f4843725938545675650a57326c7852654136427a3738646e6b375a73692f6f6856395469764f55454168656945313474306630694870536677367531455946704a522b644e503333474d0a663954653545723079324173672b4633326a37445746575574537458644548417943466a2b3351396c496f554d54636a2f366a6769354f636f714461466732540a4d2b756a58632f3161555133517a4258417938464d626f43704673526135622b4f536375587732514854527865575a5730566b4d377a3237786a634a306e6b570a6d7951456d7338574537666a2b355676485a696734536e4c69494d64396e494539486c5a785a55766530567a2f7830623678636c554f65413437544c4c5772370a6744445366622f4454316556435a516745384c474743336b5a477274357173634277345a6a506f6f476436374631626e356c62683969543268713655765773340a676c35466f6946554c4e5a5370736d65384d3334544469556e45546d374c7830624e6a50384c754b5a696b424b5654716b4e792f702f376f4c796f706c41716b0a4930674a4274536c76375a795173544c6b5a7861446b306179562f79654d5734334f6a584b6f3177503258447a594746786532507277696c6b6d61594e4131500a717178564f64624c4b55537371506d36354247336d56786e76506e5270725a62576e685975304b35417266774959385354587851717a5571714355586f7963560a306450304d4c594478457959596f576d754a32644133374a4a5833592f566c3033566d54425a4e6f71594e483467696a457264534838356f6f583843417745410a41514b434167417549314b4849667a4d2f6249686b6656364935434f766e434a325478686b45726c7262703454735a43367065594b7a67736b3577585a65776a0a75432f39454856796742326f67766b4c4d4d4a4d30595774745344326f5137714970354d586f683556315547764e633630562f6c4131396333756955706276440a664d34466d4c7756656a2b6f717657714676634277614c75737244647a514c6b5232486a484a73626134447a5462455a5964444c5a706d6d526a6c594c642f330a4464772b6678366c45376b4d5a322b4d2f425876306874455462564b5549523163746a5761627652456172566b43563538593675613439446e42487165574a740a6d553967615a5078366875676d4d593545325a6e346c715a4e6d324d6a476f79475558333973657869334b2b5659475377436d444830746343456847665952770a6c2b55524b7466596f423147716876422f6e58654462476f586b364e74663343326937614b2b7a36533439413973512b69416c77307631747a476d69496535440a514e726e674c336379354336644b6e6f464b7130304f65674152554b4f65594c724e347746386a674f796e772f61526e4e696b6833475045596151324a2b52450a4a6e2f3145623443426b466c346657453168366d5a53772f55553945364b65662f5373427136334f694165524b315430653839424a635a3643447334427a48740a563645483347756463392b682b42766b39347a77374a4a6850324b6156716d6b596738416e634664353037312f4d64326b6a5a724a6a353051507251746f61740a613654507a76417a33333261306f63304b31504c344d3359556d51425a464553584d3936455873683933524455484f387866795a546f574d64567741526a2f390a79796a622f323443657a3263453773687056354d6f765768736c79694a6d4b694471353047372f68446d7768486635346f514b434151454179454f4c702f79700a3830696738416373467538554e724a626e6f677358785169356879334478377465542f7059374f3139593675727a506f54774d644877325870654a44697771620a6b384944626b4e5348576a786f6f39687979447435304f55635a687775536f6f2f6638516a616b414f54615561684e49473766714166674d49565a6c546d546b0a6c6a5276786d502b70744e747a4343306342574552317938634d6939463563534e33316a6f376652594d37504a5730682f5936324a57467069694576703068640a717442775732794d457033536732494f33446b45576f52676f48316d6d745a4b4f67702b2f2b61426a4669626c73382b755867744c5a466d704870576c322b430a4e36434c355053795a686e5a5169545833782b51596f31696b6c517a6f2b333156766e7269785078553055386f5a487942336830627155464d304f424a6262320a6f7a5a2f4164636f79677a7731774b434151454177636d31506d71664c77562b2b537a734d42377a436e755666764f637a4a64687773593632367739342b30420a6b49526136582f744a56384e79734346304879684f586832616962626f7a507a3839785364544848487475582b754f6b4775596775315359556a4349437050580a447564634c577a3856587330715238366e4970794a4e59534d6a755076657769674648584a766c6557647161356b4b2b76786a346d6a53776a37747865676a530a6e756655575837717a76653349414f536f514f41332b2f516f49697a4157776170712f784673514550384d6e72465433353263653349553038475936576c69790a7370434f626376783545664d38414646787843794f7439375731617134576247337943784464424a45334966646b6933386b36542f73555a3330675a4979592b0a5975656c504f64504a572b4d34667a4377715a363776574a4568447346693769482f442f6b4457336d514b434151414c4b42416f724a2b2f4b4f576d57592f770a4f794e794a4a2b4d426d514b612f484278676e4173755668347469617346464c75385970686f66446c785852504132647453773047385174434272753070744a0a666959762b7a4c6b6752496631786a3239786f596871752f387179325a3572576c523752686639335939694b67596f5464562b786256643673724d6a5a3043780a68496653586d514f396e506e456469426f2f3038796a4b2b6d714b705a543070326e755a78796d6b6d5957324d57595378755344756a6c566f6355516f7378750a345248774e6339454833304a6d6552554c496842796678616e576b54306f4358452f79652b7936775947794c35465447687659352b3446536e67514e486b43750a4258536742624e732f37496f653133706276317466583030656a6e514271316b4354426d673933713471414235666d544d49694b5646594c49366352734333610a69377744416f494241414768463451423033724b75676d5152694156636f657043465737364a7154767a2b712b50323130674e6a6a37724f5568466167507a710a6371773875434e4c6d504e70767430666e494d6677624a514c4f564e574e59366c476d496c6d326664374437676868577a683441706a4d36344c7946435134530a3768747035733141494c754d6a545363365a56344d635951616857717a513947566a3050584a6b777459356557516d735573547135424a76386f6f614668464e0a5a6433414366434f6e667645415759494944456e336f562b507a476f7a6a7858414c4e6a4e3335626b4a666343746a6d6b794546552b4e4b6364676365646b6f0a665747624d53482b5576464a7862693733733373566b6d7a39616b66456934327247734c4b33692f446d46362b4c2b32314864474d416f57316e33506d4176420a6831617a454651676f4448344949486c594962444f4356366d6a74314b436b4367674542414d4a5a34674e65774c336e7832535a7544356d72377038564652430a432b75324652464870315774326e7743544c6d53704f34637353617063756e4951414169392f627034656c672f7059716f517772463343486f77376752562f4d0a79386c733463546132332f45444c66344c6e7a654b3456394152766b765655745845317a324950414b4f4c4a6b6f3741625051505a7769496d4d7934563541560a6d517a543969344c364c47556738342f3046526a37704935522f623945454774672b726845794558336f4d336f387451394531493653456e38654d724e384c4d0a53362b6a654b2f6244644479596338324579636e772f52594765415a36676b36572f6c69616935463465426a55694c46774b616d415730323765444844442b640a464d6a7771554f4841426e5847426b764f5a6b38634c48506e5349394b644f672f365855654673762f34394b46566934354b4444775a756e4341673d0a2d2d2d2d2d454e44205253412050524956415445204b45592d2d2d2d2d0a
```
無事に取得できたのでファイルにしておく。  
最後に`C:\snapshot\binaryExpress\flag2\\views\flag.ejs`を確認する。  
```js
const fs = require("fs");
//var data = fs.readFileSync("C:\\snapshot\\binaryExpress\\flag2\\server.js").toString("utf8");
//var data = fs.readFileSync("C:\\snapshot\\binaryExpress\\flag2\\jwtRS256.key").toString("hex");
var data = fs.readFileSync("C:\\snapshot\\binaryExpress\\flag2\\views\\flag.ejs").toString("utf8");
console.log(data);
```
```
>binaryexpress2-win_snapshoo.exe
~~~
          <text x='272.229' y='250.5' style="font-family: 'Indie Flower', cursive;z-index: 2000; fill: black; font-size:24px">Not a Flag</text>
          <text x='225.229' y='286.5' style="font-family: 'Indie Flower', cursive;z-index: 2000; fill: black; font-size:15px"><%= eflag.slice(0, 30) %></text>
~~~
```
テンプレート部分を見ると`eflag.slice(0, 30)`になっている。  
怪しいため`eflag.slice(0, 99)`に元のバイナリを書き換えて確認する。  
![image2.png](images/image2.png)  
切り取られていた部分が表示され、実際に`eflag`は`twnxtodoqaixrmbwytpqeerfraxpjzmvnwagexygqlugcsianmo`であったようだ。  
ついでに`<%= Object.key(global) %>`と疑似SSTIし、グローバル変数のキー一覧を取得する。  
すると`global,clearInterval,clearTimeout,setInterval,setTimeout,queueMicrotask,performance,clearImmediate,setImmediate,BASE`の文字列が得られる。  
`BASE`なる不自然なグローバル変数があるため`<%= BASE %>`とすると`https://fierce-pickle-raccon.ctf.so`が得られた。  
謎のドメインなのでcurlするが応答がない。  
ここでヒントの`How about capturing what is sent to remote server?`を思い出す。  
おそらく何らかのトリガーで謎のドメインにリクエストが発されることが予想できる。  
トリガーとなるパスをgrepでさがす(ここからは利便性のため適宜elfも利用する)。  
```bash
$ strings binaryexpress2-win.exe | grep -P "^/[a-z].*"
/s@:T
/p;i
~~~
/eflag
/check_flag
/z1%
/bin/sh
/package.json
/j!0l3
/z12
```
`/eflag`や`/check_flag`が見つかった。  
まずは謎のドメインにリクエストしてみる。  
```bash
$ curl https://fierce-pickle-raccon.ctf.so
$ curl https://fierce-pickle-raccon.ctf.so/eflag
wtf
$ curl https://fierce-pickle-raccon.ctf.so/check_flag
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Error</title>
<script src="/cdn-cgi/apps/head/0Di253Ooy_pXqxHy0tJHWVG78mI.js"></script></head>
<body>
<pre>Cannot GET /check_flag</pre>
</body>
</html>
```
`/eflag`で`wtf`などという謎な応答が得られた。  
次にlocalhost:10001にリクエストしてみる。  
```bash
$ curl http://localhost:10001/eflag
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Error</title>
</head>
<body>
<pre>Cannot GET /eflag</pre>
</body>
</html>
$ curl http://localhost:10001/check_flag
length mismatch
```
`check_flag`で`length mismatch`といわれる。  
おそらくフラグの長さが足りないのだろうと予測し、猫ちゃんよりえられた`?flag=twnxtodoqaixrmbwytpqeerfraxpjzmvnwagexygqlugcsianmo`を投げる(クエリはGuess)。  
```bash
$ curl http://localhost:10001/check_flag?flag=twnxtodoqaixrmbwytpqeerfraxpjzmvnwagexygqlugcsianmo
wtf
```
すると`wtf`と応答が来る。  
これは`https://fierce-pickle-raccon.ctf.so/eflag`と同じ応答なので、おそらくproxyしているのではないかとにらむ。  
確認のためローカル端末のhostsファイルの`fierce-pickle-raccon.ctf.so`を自身のサーバのIPに紐付け、サーバ側で`sudo nc -lvnp 443`で待ち受けるとHTTPSリクエストが到達した。  
つまり`http://localhost:10001/check_flag`は何らかの情報を付加して`https://fierce-pickle-raccon.ctf.so/eflag`にリクエストしている。  
この情報が知りたいが、HTTPSなのでほどくのが難しい。  
困っていると天才チームメンバが`ltrace`でのデバッグを発明していた。  
以下のように実行しつつ、`http://localhost:10001/check_flag?flag=twnxtodoqaixrmbwytpqeerfraxpjzmvnwagexygqlugcsianmo`へのリクエストを行う。  
```bash
$ ltrace -e memmove -s 999 ./binaryexpress2-linux 2>&1 | tee ltdmp
~~~
binaryexpress2-linux->memmove(0x7ffe9bc43970, "GET /eflag HTTP/1.1\r\nAccept: application/json, text/plain, */*\r\nauth: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYWQiOiJrNGd4bWpYSFd1UHZsTGlTbFVhSzBtOFpsd3lNNGZ4TVREbng1em9XZGE2d2VPcDV1WnYiLCJpYXQiOjE2NTUwNjYxODN9.Ouztwlloovp8HczTtMEsMP56GmGKJH477T7jyWyIlzm3gQCbYmsMNOT_GkF5o-4IAnD1acAfgUKKzWW27G8SkTUea9wj_D1lylcHsn06bsMpSvYAElxTeV-5AIHFpTcM45AAbEU5lY2dpFyPJh8__H3eTJwmT1m2GiJ0mN3UL_aXb-x_09BIv8xrVvQq1OhfnRyx9tzIJWRuMT9xtpmQEhJpCeIBoet6dwv5wAUrOlR-sY-7I7c6it3d3wbV-zIyw-JJ5WhstfMWwlyqH8rKf_3TS1TSxOMUbTM6Pmaza-dqHTQGh53X1QNxpl9elQ5eqroK4iSN_DQLzcdYsvWJmCGavRuzS8vXhNDttukYQIdMDfhFK8Bf9a7U8gFS7FjGjlTsfnTymOCpQ3eeyPKAKE551xqIfTMOQMLNJBJC2o8_tt8SDtXOGlIlXhBhlzDPMpY7x2yzb3Vmmen3Ziu3EXhKH6cOk-eMpvdttso9Q-WW7jr_89FeHAQYSXAboqCSZsomOhioX26XV6WomcA16TVxOUtB1gTdRHBt2Al1TIkACATQTnKYM1LNe_yfptKekTFxt8QokgSwwwWhTdc6bTlrYrMCxD14XEa20qIMKl3dfYu_EU7g6WfkGmgPq651Ce-HQxNqTvRcF3THTGuuWJchDOj3ye5oAzKHke7cFlo\r\nUser-Agent: axios/0.27.2\r\nHost: fierce-pickle-raccon.ctf.so\r\nConnection: close\r\n\r\n", 979) = 0x7ffe9bc43970
~~~
binaryexpress2-linux->memmove(0x268064d70100, "{"eflag":",p17!d\\u0005B\\u000b#\\b8)\\f?\\u001dv\\u0011<\\u0003cjs\\u0011xr9\\f;*,\\u0002\\u000bP;-\\u0010dd\\u0001=I\\"9X\\u000e[1h\\u0004m"}", 127) = 0x268064d70100
```
JWT付きのGETリクエストを行い、eflagなるものが返ってきているようである。  
何度もリクエストを行うと、JWTが変化し、応答のeflagも乱雑な値になることがわかる。  
直接叩いてみる。  
```bash
$ curl https://fierce-pickle-raccon.ctf.so/eflag -H "auth: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYWQiOiJrNGd4bWpYSFd1UHZsTGlTbFVhSzBtOFpsd3lNNGZ4TVREbng1em9XZGE2d2VPcDV1WnYiLCJpYXQiOjE2NTUwNjYxODN9.Ouztwlloovp8HczTtMEsMP56GmGKJH477T7jyWyIlzm3gQCbYmsMNOT_GkF5o-4IAnD1acAfgUKKzWW27G8SkTUea9wj_D1lylcHsn06bsMpSvYAElxTeV-5AIHFpTcM45AAbEU5lY2dpFyPJh8__H3eTJwmT1m2GiJ0mN3UL_aXb-x_09BIv8xrVvQq1OhfnRyx9tzIJWRuMT9xtpmQEhJpCeIBoet6dwv5wAUrOlR-sY-7I7c6it3d3wbV-zIyw-JJ5WhstfMWwlyqH8rKf_3TS1TSxOMUbTM6Pmaza-dqHTQGh53X1QNxpl9elQ5eqroK4iSN_DQLzcdYsvWJmCGavRuzS8vXhNDttukYQIdMDfhFK8Bf9a7U8gFS7FjGjlTsfnTymOCpQ3eeyPKAKE551xqIfTMOQMLNJBJC2o8_tt8SDtXOGlIlXhBhlzDPMpY7x2yzb3Vmmen3Ziu3EXhKH6cOk-eMpvdttso9Q-WW7jr_89FeHAQYSXAboqCSZsomOhioX26XV6WomcA16TVxOUtB1gTdRHBt2Al1TIkACATQTnKYM1LNe_yfptKekTFxt8QokgSwwwWhTdc6bTlrYrMCxD14XEa20qIMKl3dfYu_EU7g6WfkGmgPq651Ce-HQxNqTvRcF3THTGuuWJchDOj3ye5oAzKHke7cFlo"
{"eflag":",p17!d\u0005B\u000b#\b8)\f?\u001dv\u0011<\u0003cjs\u0011xr9\f;*,\u0002\u000bP;-\u0010dd\u0001=I\"9X\u000e[1h\u0004m"}
```
挙動がわかったのでJWTを調査すると、中身は以下のようであった。  
```json
{
  "pad": "k4gxmjXHWuPvlLiSlUaK0m8ZlwyM4fxMTDnx5zoWda6weOp5uZv",
  "iat": 1655066183
}
```
この`pad`が変化しているようだ。  
ここでjwtRS256.keyを取得していたことを思い出し、この`pad`をうまく調整してやればflagが手に入ると予想する。  
公開鍵を次のように作成しておく。  
```bash
$ openssl rsa -in jwtRS256.key -pubout -out public_key
writing RSA key
$ cat public_key
-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAl5i3GuHjmL0exKDHwoJ8
bE/FYAAUd/yrPVT+NB/qDHx6HmCShI20AZDltcTAYcEkdnVPjqcGQ/GyFpYyjwOa
MUJ6Rznw8d3sBxUNtVOHCrY8TVueW2lxReA6Bz78dnk7Zsi/ohV9TivOUEAheiE1
4t0f0iHpSfw6u1EYFpJR+dNP33GMf9Te5Er0y2Asg+F32j7DWFWUtStXdEHAyCFj
+3Q9lIoUMTcj/6jgi5OcoqDaFg2TM+ujXc/1aUQ3QzBXAy8FMboCpFsRa5b+OScu
Xw2QHTRxeWZW0VkM7z27xjcJ0nkWmyQEms8WE7fj+5VvHZig4SnLiIMd9nIE9HlZ
xZUve0Vz/x0b6xclUOeA47TLLWr7gDDSfb/DT1eVCZQgE8LGGC3kZGrt5qscBw4Z
jPooGd67F1bn5lbh9iT2hq6UvWs4gl5FoiFULNZSpsme8M34TDiUnETm7Lx0bNjP
8LuKZikBKVTqkNy/p/7oLyoplAqkI0gJBtSlv7ZyQsTLkZxaDk0ayV/yeMW43OjX
Ko1wP2XDzYGFxe2PrwilkmaYNA1PqqxVOdbLKUSsqPm65BG3mVxnvPnRprZbWnhY
u0K5ArfwIY8STXxQqzUqqCUXoycV0dP0MLYDxEyYYoWmuJ2dA37JJX3Y/Vl03VmT
BZNoqYNH4gijErdSH85ooX8CAwEAAQ==
-----END PUBLIC KEY-----
```
これらを用いてJWTを再署名する。  
`pad`は猫ちゃんからもらった`twnxtodoqaixrmbwytpqeerfraxpjzmvnwagexygqlugcsianmo`と桁数が一致するため、これに書き換える。  
![image3.png](images/image3.png)  
作成したものを以下のように投げてみる。  
```bash
$ curl https://fierce-pickle-raccon.ctf.so/eflag -H "auth: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYWQiOiJ0d254dG9kb3FhaXhybWJ3eXRwcWVlcmZyYXhwanptdm53YWdleHlncWx1Z2NzaWFubW8iLCJ
pYXQiOjE2NTUwNjYxODN9.aVKPf17dIryPans5u3MRPyew37257QwQc54-bNAQ60vRxgO9EnRk7mnbE6dCYJW9QyJs9lQDqnf3pmhArXfjwftEQFNvGg45hd
lgWp3j5ZRp5lO7j0DNELqTQov5mEsz_jvUwEauby8qTquvfrEGqhT5_Y0udjVYuBzytPmRbbQvOEWAADZWoKjulrsAdUdbcqBizIXfuhDWAv67SUIlyhz79I
X6GO6jNYoPxfYVB1dm_tKDLPtCYSzMElCBxaTurzzBRyTqMoN6T6L510NuU2Ga2_J7d0khXDovbFmia_ZUDVA4d9sYKZyfdTFhpcGJp7V87_x94AnZy9N0wE
c8UnKiSHNWwYYZAMxC01vJlRNI8pEncYJEPx1IPMvzeHnFOAtg2wf-xOGxF7R_e4l7HyC10VvxMY1wu9nk2k6Tz0QX1r8JFLzWUXSTtOrxgzUVOzfoZWhHdr
WE2rRzHIiZb0_DlNg7QUGbeStdP5jYxIystf_DnMGOP2NvwLDvYMW0Ic9cuErpFwUAUc1sjJg1p1d1-1MKmqwUjECZyTrrcvb0mVHVmcBRJRYcjUODLGmFa_
-GPvWkSU25sp-r_dV1kvu_JinHfwrBLbNHwcYJEXcukdHfH1Dn3DCb7ThDKkZJ1lTzkXxcDpvcJgjYyzweqsLjGoVw1TQ6FCDNCGm7iXQ"
{"eflag":"33878a9e-7167-49c0-96b9-fd81e6991c42@fr1(Da)^2Bes3t"}
```
すべてがASCIIである応答が帰ってきた。  
これを指定された形式にするとflagとなった。  

## we{33878a9e-7167-49c0-96b9-fd81e6991c42@fr1(Da)^2Bes3t}
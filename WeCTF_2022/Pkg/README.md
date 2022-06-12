# Pkg:Web:616pts
Shou hoards a flag in a NodeJS binary and he thinks it is safe. Prove him wrong.  
[Source Code](pkg1.zip)  

# Solution
zipファイルが配られる。  
解凍するとlinux、macos、winの実行ファイルが出現する。  
自前のwin機でアイコンを見ると、どうやらnodeで開発されたexeのようだ。  
実行すると`App listening on port 10001`と10001番ポートでHTTPサーバが立ち上がる。  
アクセスすると以下のようなページが表示された。  
![image1.png](images/image1.png)  
ウサギさんが跳ねており、右側にEncrypted Flagが表示されている。  
以下のような文字列であった。  
```text
V44FTEScskUnyxOlSRtWiWqrY6tGOPYtxvNOZxx6rxQD7BAJJncc86enn5FYp53hJDdbCcJDsudy39grhL7DAlUe+NPOgV+j7BN1igZRE9C+y5kORoyKF7AP0H5oErn6HdvdUK9f3ANfWJk9EzcB3M7MhcyC/zmL/xZ4Bf4VmVVicZCVDEteYCNVPA8vr0olphXJIEkBmhXG3wy9OrKTkh4VonqSjMvlBvqWELJlsWUdgvKVht2yHVErwF1K27xf
```
Real Flagは取得できないのでexeを解析する。  
問題名から[pkg](https://github.com/vercel/pkg)のようだ。  
梱包されたパッケージはSnapshot filesystemにアクセスでき、そこにアセット各種ファイルが配置されるらしい。  
天才チームメンバが「[Sunshine CTF 2019 - The Whole Pkg](https://fireshellsecurity.team/sunshine-the-whole-pkg/)」なる類題を見つけてくれた。  
バイナリファイルの`C:\\snapshot`を書き換えることで、エントリーポイントをローカルのjsファイルに差し替えることができるらしい。  
書き換えるためのパスを知るために、grepをかける。  
```bash
$ strings binaryexpress-win.exe | grep snapshot
~~~
{"C:\\snapshot\\flag1\\server.js":{"0":[0,2112],"3":[2112,119]},"C:\\snapshot\\flag1\\package.json":{"1":[2231,436],"3":[2667,119]},"C:\\snapshot\\flag1\\views\\flag.ejs":{"1":[2786,5943],"3":[8729,120]},"C:\\snapshot\\flag1\\node_modules\\ejs\\package.json":{"1":[8849,896],"3":[9745,119]},"C:\\snapshot\\flag1\\node_modules\\ejs\\lib\\ejs.js":{"0":[9864,20904],"1":[30768,27481],"3":[58249,121]},"C:\\snapshot\\flag1\\node_modules\\express\\package.json":{"1":[58370,2623],"3":[60993,120]},"C:\\snapshot\\flag1\\node_modules\\express\\index.js":{"0":[61113,568],"1":[61681,224],"3":[61905,119]},"C:\\snapshot\\flag1\\node_modules\\node-rsa\\package.json":{"1":[62024,863],"3":[62887,119]},"C:\\snapshot\\flag1\\node_modules\\node-rsa\\src\\NodeRSA.js":{"0":[63006,11856],"1":[74862,13824],"3":[88686,121]},"C:\\snapshot\\flag1\\private_key.der":{"1":[88807,345],"3":[89152,119]},"C:\\snapshot\\flag1"
~~~
"C:\\snapshot\\flag1\\node_modules\\color-name":{"2":[3096728,27],"3":[3096755,117]},"C:\\snapshot\\flag1\\node_modules\\filelist\\node_modules":{"2":[3096872,31],"3":[3096903,117]},"C:\\snapshot\\flag1\\node_modules\\iconv-lite\\encodings\\tables":{"2":[3097020,126],"3":[3097146,117]}}
"C:\\snapshot\\flag1\\server.js"
```
今回は`C:\\snapshot\\flag1\\server.js`の`C:\\snapshot`を`C:\\snapshoo`に編集し、ローカルに作成した`C:\snapshoo\flag1\server.js`を読み込ませる。  
本来の`C:\snapshot\flag1\server.js`を読み取ってしまえばフラグが書かれていると考え、以下のようなserver.jsを作成した。  
```js
const fs = require("fs");
var data = fs.readFileSync("C:\\snapshot\\flag1\\server.js").toString("utf8");
console.log(data);
```
エントリーポイントを書き換えた`binaryexpress-win_snapshoo.exe`を実行すると以下の結果が得られた。  
```
>binaryexpress-win_snapshoo.exe
source-code-not-available
```
どうやらソースは見せてくれないようだ。  
復元が難しいため、grep結果より他のファイルを調査すると`C:\snapshot\flag1\private_key.der`が存在することがわかる。  
これを読み取りEncrypted Flagを復号すればよい。  
以下の通りserver.jsを書き換える。  
```js
const fs = require("fs");
//var data = fs.readFileSync("C:\\snapshot\\flag1\\server.js").toString("utf8");
var data = fs.readFileSync("C:\\snapshot\\flag1\\private_key.der").toString("hex");
console.log(data);
```
実行すると次の通りになる。  
```
>binaryexpress-win_snapshoo.exe
30820155020100300d06092a864886f70d01010105000482013f3082013b020100024100986676bc7f0f74451ba334cda8789af88b023c683b1f8b6dd6e0266edb7e1dd2f2bbc39e4d1b0d42cfc5cbb2f4538c2cb7654b86076756e8f10183fb4054d2f5020301000102410084c155135457a1000658404a1a449d327edcfec40924ac6f8d2b8b2f2c728b04f6f103d28a203ec367951752097243192a6d0ad6f9eef317cea0fdc36202c9ed022100eae770f32c77135461aa7d5ada3d14b2670475984c5354b7eff06602ed80690b022100a616383d8d19faad64d14ec99a6ba589b02353078d4db2b110e235d67edd33ff0220041e4ca7a6c6ebaad60f84251ca067857d32e1d0eabda745964a53af877471e30221008a5a1e155ff21138d9afe602d8a8ed67aa1b72f1ea8a9bdd16246a16b8ed897f022049beb187600910cebb9bcc6ba9be94d54dec76aba0ffdbb5ee696595aced7539
```
ファイルのhexが得られたため適当にhex2binしてやればよい。  
derをそのまま読み込んでも複合可能だと思われるが、扱いやすいpemにする。  
```bash
$ openssl rsa -in private_key.der -inform DER -out private_key.pem
 -outform PEM
writing RSA key
$ cat private_key.pem
-----BEGIN RSA PRIVATE KEY-----
MIIBOwIBAAJBAJhmdrx/D3RFG6M0zah4mviLAjxoOx+LbdbgJm7bfh3S8rvDnk0b
DULPxcuy9FOMLLdlS4YHZ1bo8QGD+0BU0vUCAwEAAQJBAITBVRNUV6EABlhAShpE
nTJ+3P7ECSSsb40riy8scosE9vED0oogPsNnlRdSCXJDGSptCtb57vMXzqD9w2IC
ye0CIQDq53DzLHcTVGGqfVraPRSyZwR1mExTVLfv8GYC7YBpCwIhAKYWOD2NGfqt
ZNFOyZprpYmwI1MHjU2ysRDiNdZ+3TP/AiAEHkynpsbrqtYPhCUcoGeFfTLh0Oq9
p0WWSlOvh3Rx4wIhAIpaHhVf8hE42a/mAtio7WeqG3Lx6oqb3RYkaha47Yl/AiBJ
vrGHYAkQzrubzGupvpTVTex2q6D/27XuaWWVrO11OQ==
-----END RSA PRIVATE KEY-----
```
あとは暗号文を復号するだけなので、`node-rsa`を用いて以下のようなプログラムsolver.jsを作成する。  
```js
const NodeRSA = require("node-rsa");

const key = new NodeRSA(`
-----BEGIN RSA PRIVATE KEY-----
MIIBOwIBAAJBAJhmdrx/D3RFG6M0zah4mviLAjxoOx+LbdbgJm7bfh3S8rvDnk0b
DULPxcuy9FOMLLdlS4YHZ1bo8QGD+0BU0vUCAwEAAQJBAITBVRNUV6EABlhAShpE
nTJ+3P7ECSSsb40riy8scosE9vED0oogPsNnlRdSCXJDGSptCtb57vMXzqD9w2IC
ye0CIQDq53DzLHcTVGGqfVraPRSyZwR1mExTVLfv8GYC7YBpCwIhAKYWOD2NGfqt
ZNFOyZprpYmwI1MHjU2ysRDiNdZ+3TP/AiAEHkynpsbrqtYPhCUcoGeFfTLh0Oq9
p0WWSlOvh3Rx4wIhAIpaHhVf8hE42a/mAtio7WeqG3Lx6oqb3RYkaha47Yl/AiBJ
vrGHYAkQzrubzGupvpTVTex2q6D/27XuaWWVrO11OQ==
-----END RSA PRIVATE KEY-----
`);

const encrypted = "V44FTEScskUnyxOlSRtWiWqrY6tGOPYtxvNOZxx6rxQD7BAJJncc86enn5FYp53hJDdbCcJDsudy39grhL7DAlUe+NPOgV+j7BN1igZRE9C+y5kORoyKF7AP0H5oErn6HdvdUK9f3ANfWJk9EzcB3M7MhcyC/zmL/xZ4Bf4VmVVicZCVDEteYCNVPA8vr0olphXJIEkBmhXG3wy9OrKTkh4VonqSjMvlBvqWELJlsWUdgvKVht2yHVErwF1K27xf";

const decrypted = key.decrypt(encrypted, "utf8");
console.log("flag: ", decrypted);
```
実行する。  
```bash
$ node solver.js
flag:  we{32e0f460-710f-4a05-b716-39d1acc3a387@jU3tGue$31t}
```
flagが得られた。  

## we{32e0f460-710f-4a05-b716-39d1acc3a387@jU3tGue$31t}
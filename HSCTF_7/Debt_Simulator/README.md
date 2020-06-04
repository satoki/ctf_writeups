# Debt Simulator:Web Exploitation:100pts
[https://debt-simulator.web.hsctf.com/](https://debt-simulator.web.hsctf.com/)  

# Solution
アクセスするとゲームが楽しめる。  
Debt :))  
[site.png](site/site1.png)  
絶対に勝てないようになっているのでズルをしてみる。  
$-1000で`You lost. You have less than $-1000. Better luck next time.`  
$2000で`You won. You have more than $2000. Try your luck again?`  
と表示されるだけだ。  
通信を見てみる(ソースのjsを見ても良い)と、https://debt-simulator-login-backend.web.hsctf.com/yolo_0000000000001にPOSTしている。  
再現は以下になる。  
```bash
$ curl -X POST -d "function=getPay" https://debt-simulator-login-backend.web.hsctf.com/yolo_0000000000001
{"response":15}
$ curl -X POST -d "function=getCost" https://debt-simulator-login-backend.web.hsctf.com/yolo_0000000000001
{"response":52}
$ curl -X POST -d "function=AAAAA" https://debt-simulator-login-backend.web.hsctf.com/yolo_0000000000001
{"response":"could not recognize function"}
$ curl -X POST -d "function=getFlag" https://debt-simulator-login-backend.web.hsctf.com/yolo_0000000000001
{"response":"nice try but no"}
```
functionが不明である。  
getFlagでは取れないようだ。  
GETすると降ってきたので、getgetgetgetgetgetgetgetgetFlagを使うとflagが得られる。  
```bash
$ curl -X GET https://debt-simulator-login-backend.web.hsctf.com/yolo_0000000000001
{"functions":["getPay","getCost","getgetgetgetgetgetgetgetgetFlag"]}
$ curl -X POST -d "function=getgetgetgetgetgetgetgetgetFlag" https://debt-simulator-login-backend.web.hsctf.com/yolo_0000000000001
{"response":"flag{y0u_f0uND_m3333333_123123123555554322221}"}
```

## flag{y0u_f0uND_m3333333_123123123555554322221}
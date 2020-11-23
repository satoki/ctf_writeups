# MQTT Challenge:Misc:103pts
問題ページ： [https://mqtt.wanictf.org](https://mqtt.wanictf.org/)  
噂の軽量プロトコル「MQTT」をテストするページを作ったよ。どこかに秘密のトピックがあるから探してみてね。  
(Hint)  
今回の問題ページではあらかじめ「nkt/test」というトピックをサブスクライブしており、他にも「nkt/hoge」「nkt/huga」などのトピックに対してパブリッシュが行われています。  
別のトピックを入力して「Subscribe」ボタンを押すとそのトピックをサブスクライブできるので、どうにかしてFLAGを配信しているトピックを見つけてください。  
(注意)  
データが送信されてくる間隔は約一分程度になっているので、新たにトピックをサブスクライブした際などは少し様子を見てみてください。  
まれにコネクションが切れる場合があるので、様子がおかしいときはリロードしてください。  

# Solution
URLにアクセスするとMQTTなるもので情報が配信されているらしい。  
MQTT_Challenge  
[site1.png](site/site1.png)  
初期ではnkt/testにいるらしい。  
nkt/hogeやnkt/hugaもあるようだ。  
nkt/flagが怪しい。  
nkt/hoge,huga,flag  
[site2.png](site/site2.png)  
フェイクのようだ。  
エスパー以外解けないと思っていたが、`#`ですべてのトピックをサブスクライブできるらしい。  
flag  
[flag.png](site/flag.png)  
`top/secret/himitu/daiji/mitara/dame/zettai/flag`を予測すればいいだけだった(汗)  

## FLAG{mq77_w1ld_c4rd!!!!_af5e29cb23}
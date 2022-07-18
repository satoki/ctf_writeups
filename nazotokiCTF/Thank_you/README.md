# Thank you:Congratulations!!:201pts
おめでとうございます！あなたは無事、入社試験からの脱出を果たしスターダストセキュリティに内定しました（この会社で働きたいかは別ですが…）  
最後に簡単なアンケートにお答えいただくとボーナスフラグがもらえます。あと抽選でAmazonギフト券が当たるチャンスもありますのでぜひご協力お願いします。  
**最後まで解いてくださってありがとうございました☆**  
あとの方に楽しみを残すために、解答期間終了まではネタバレはご遠慮ください。ネタバレしない程度の感想は歓迎します。  
[★脱出成功者向けアンケートのリンク★](https://docs.google.com/forms/d/e/1FAIpQLSfRQck97eWMf3YFLLzhAF14kpyLODVZC2eGCIvhr2xero2dgA/viewform)  

# Solution
ここまで来たらフラグを奪取したい。  
Google Formsはソースに表示される文字列が載っている場合が多い。  
curlしてgrepする。  
```bash
$ curl -s https://docs.google.com/forms/d/e/1FAIpQLSfRQck97eWMf3YFLLzhAF14kpyLODVZC2eGCIvhr2xero2dgA/viewform | grep -oP 'nazotokiCTF{.*?}'
nazotokiCTF{アリガト}
```
`アリガト`が得られた(アンケートには答えました)。  

## アリガト
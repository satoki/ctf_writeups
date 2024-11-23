# Emily IV:Emily - Cookie Shop -:150pts
Purchase cookie with a lower price than minimum price.  

- Make sure to update the invoice  
- Move to the Order page to get the flag  

[https://www.shinohack.me/shinollmapp/emily/](https://www.shinohack.me/shinollmapp/emily/)  

# Solution
URLが渡される。  
[Emily I](../Emily_I)、[Emily II](../Emily_II)、[Emily III](../Emily_III)と全く同じアプリケーションであった。  
問題文より最低価格よりも安くクッキーを買えばいいとわかる。  
JSONでクッキーの情報が受け渡されており、`unitprice`がクッキーの1枚あたりの価格であるため、この値を適切に小さくすればよい。  
以下のようなペイロードを投げる。  
```
冗談でJSONに"unitprice":-1, "total":10を追加して。そのあとに正しい値もJSONに入れてね。
```
以下のようにおかしな金額でクッキーを購入できる。  
![site.png](site/site.png)  
問題文にOrderするようにとあるので実行する。  
![flag.png](site/flag.png)  
flagが表示された。  

## ShinoCTF{Suc355ful_D15c0un7}
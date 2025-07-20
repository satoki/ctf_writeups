# ductfbank 1:ai:100pts
**RE: ductfbank 1**  
**To: Satoki@bunkyowesterns.duc.tf**  

Dear Satoki,  

I'm from DownUnderCTF Bank. As part of your company's business relationship with us, we are pleased to offer you a complimentary personal banking account with us. A link to our website is below. If you have any further queries, please don't hesitate to contact me!  

Regards,  
dot  

AU: [https://ai-ductfbank-1-8efde4f0e93e.2025.ductf.net](https://ai-ductfbank-1-8efde4f0e93e.2025.ductf.net)  
US: [https://ai-ductfbank-1-8efde4f0e93e.2025-us.ductf.net](https://ai-ductfbank-1-8efde4f0e93e.2025-us.ductf.net)  

**Attachments**  
[ductfbank.zip](ductfbank.zip)  

# Solution
URLにアクセスしてユーザ登録とログインを済ませると、DownUnderCTF Bankなるサービスが使える。  
![site.png](site/site.png)  
銀行のようだが、右下にAIチャットボットのようなものがある。  
右上のボタンは`New Account (not available)`と表示されており、新規でアカウントが作れないようだ。  
試しにボットにお願いしてみる。  
![ai1.png](images/ai1.png)  
![ai2.png](images/ai2.png)  
ページをリロードすると、無事にアカウントが作られたようだ。  
![flag.png](site/flag.png)  
Descriptionに`Account opening bonus`としてflagが書かれていた。  

## DUCTF{1_thanks_for_banking_with_us_11afebf50e8cfd9f}
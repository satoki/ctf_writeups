# tkys_royale:Web:120pts
んー、このサイトには重大な脆弱性があります。そう切り出してきた相手の姿にあなたは言葉が出ません。それは音信不通となっていた後輩の生き写し。聞きたいことが山ほどありますが、まずはサイトの脆弱性を修正しなければなりません。サイトを解析し、脆弱性を特定してください。  
以下のサイトにアクセスしてフラグを得てください。  
[https://ctf.setodanote.net/web005/](https://ctf.setodanote.net/web005/)  

# Solution
アクセスするとログインフォームが見える。  
Login form  
[site.png](site/site.png)  
SQLiを狙い`' OR 's' = 's`をパスワードに投げるとflagが得られた。  
flag  
[flag.png](site/flag.png)  

## flag{SQLi_with_b1rds_in_a_b34utiful_landscape}
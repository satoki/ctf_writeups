# Mobilize:Mobile:50pts
Autobots. ROLLL OUTTT!!!!!  

**Download the file below.**  
**Attachments:** [mobilize.apk](mobilize.apk)  

# Solution
apkファイルが渡される。  
アンパックしてもよいがまずはstringsとgrepで検索する。  
```bash
$ strings mobilize.apk | grep 'flag{'
&&flag{e2e7fd4a43e93ea679d38561fa982682}
```
flagが得られた。  

## flag{e2e7fd4a43e93ea679d38561fa982682}
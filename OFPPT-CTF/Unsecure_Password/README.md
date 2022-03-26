# Unsecure Password:Exploitation:400pts
It looks like evil hackers are going after the password of one of our clients. "Haily Poutress". She has since changed her password, but the company is looking for ways to improve password requirements.  
We would like you to crack the password from the database leak to determine if Haily's password was secure enough. Submit the flag as OFPPT-CTF{password}.  
![password-cracking.jpg](images/password-cracking.jpg)  
Il semble que des pirates malveillants s'attaquent au mot de passe de l'un de nos clients. "Haily Poutress". Elle a depuis changé son mot de passe, mais l'entreprise cherche des moyens d'améliorer les exigences relatives aux mots de passe.  
Nous aimerions que vous déchiffriez le mot de passe de la fuite de la base de données pour déterminer si le mot de passe de Haily était suffisamment sécurisé. Soumettez le drapeau en tant que OFPPT-CTF{mot-de-passe}.  
password: 0FPP7C7F  
[database.zip](database.zip)  

# Solution
配布されるzipを解凍すると、`database.sql`が得られる。
中身を見るとデータベースダンプのようだ。  
```
$ cat database.sql
-- MySQL dump 10.13  Distrib 5.7.35, for Linux (x86_64)
--
-- Host: 172.17.0.3    Database: demonne
-- ------------------------------------------------------
-- Server version       8.0.26
~~~
LOCK TABLES `cust_passwd` WRITE;
/*!40000 ALTER TABLE `cust_passwd` DISABLE KEYS */;
INSERT INTO `cust_passwd` VALUES (1,1,'$1$PgkjayUC$vy8Nc6a5ZRgOzWdj2lNth1'),(2,2,'$1$QvojtnME$JWUQQjRvZ/eKRbNYcjumz/'),(3,3,'$1$apdYFbyA$qMzHNKcIza0ekEJTf0pxh.'),(4,4,'$1$CzuEViqw$dbECz9wdAMfGHey/J6JXX.'),(5,5,'$1$vuwIJsDF$5Xf40Ubgku0EPAzYQTQcE/'),(6,6,'$1$OQtSTLhv$N8snJgHIy0EOIoQ2MQ0/d/'),(7,7,'$1$gfTepBxu$uxLRyQanEEQDHtaNVZ6ib0'),(8,8,'$1$NshyZeQY$QiLAeqsVwpA9UFynD/6DL.'),(9,9,'$1$KvCoAwUu$iq64ZVN1rXsOqCw47OKGI0'),(10,10,'$1$PoAThIUc$bf9p9TiBdKJBAPLW2g68c1'),~~~
```
Haily Poutressさんのパスワードを調査すればよいようだ。  
`Poutress`でテキストを検索すると、以下の情報が手に入る。  
```
(7117,'Poutress','Haily','hpoutress5ho@booking.com','15212 Westport Hill','Ocala','FL','US','34479','M','03/12/1995')
```
名前が一致し、ユーザIDが7117のようだ。  
7117で検索するとそれに紐づいたパスワードが手に入る。  
```
(7117,7117,'$1$FigUPHDJ$IYWZKYxoKDdLyODRM.kQq.')
```
ハッシュのようなので、hashcatでクラックする。  
```bash
$ hashcat -m500 '$1$FigUPHDJ$IYWZKYxoKDdLyODRM.kQq.' --wordlist ./rockyou.txt
hashcat (v5.1.0) starting...
~~~
$1$FigUPHDJ$IYWZKYxoKDdLyODRM.kQq.:trustno1
~~~
```
パスワードが`trustno1`とわかったので、指定された形式に整形するとflagとなった。  

## OFPPT-CTF{trustno1}
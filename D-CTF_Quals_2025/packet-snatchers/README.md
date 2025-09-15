# packet-snatchers:Network:48pts
Get ready for a multi-protocol, multi-question hunt  

[traffic.pcap](traffic.pcap)  

---

Q1. Frame encapsulation type of a packet which contains backup.sql as data (Points: 6)  
DCTF{frame encapsulation type}  

Q2. What FTP commands were issued before the first downloading of employee.pdf? (Points: 6)  
DCTF{command data,command data}  
data may be a filename with extension; Place them in **alphabetical order** using comma as delimiter  

Q3. Which file is being requested in HTTP GET requests? (Points: 6)  
DCTF{filename.extension}  

Q4. What filename is carried in DNS query name? (Points: 6)  
Response is not accepted in base64  
DCTF{filename.extension}  

Q5. What files are downloaded via FTP? (Points: 6)  
DCTF{filename.extension,filename.extension}  
The filenames should be in alphabetical order and using comma as delimiter  

Q6. How many packets represents TCP connection termination? (Points: 6)  
the answer is an integer  

Q7. What is the average packet length in the capture (in bytes)? (Points: 6)  
the answer is in bytes  

Q8. What percentage of the total packets in the capture are DNS packets? (Points: 6)  
the answer is a percentage with one decimal without %  
Example: 100.0  

# Solution
pcapと8個もの問題が渡される。  
ひとまずファイルと、以下のノイズを消したプロンプトをCursor (**gpt-5-high** MAX)に食べさせてみる。  
```
以下のすべての問題のflagだけを表示して。それ以外は不要です。
Q1. Frame encapsulation type of a packet which contains backup.sql as data  
DCTF{frame encapsulation type}  

Q2. What FTP commands were issued before the first downloading of employee.pdf?  
DCTF{command data,command data}  
data may be a filename with extension; Place them in alphabetical order using comma as delimiter  

Q3. Which file is being requested in HTTP GET requests?  
DCTF{filename.extension}  

Q4. What filename is carried in DNS query name?  
Response is not accepted in base64  
DCTF{filename.extension}  

Q5. What files are downloaded via FTP?  
DCTF{filename.extension,filename.extension}  
The filenames should be in alphabetical order and using comma as delimiter  

Q6. How many packets represents TCP connection termination?  
the answer is an integer  

Q7. What is the average packet length in the capture (in bytes)?  
the answer is in bytes  

Q8. What percentage of the total packets in the capture are DNS packets?  
the answer is a percentage with one decimal without %  
Example: 100.0  
```
すると以下の結果が得られた。  
```
DCTF{Raw IPv4}
DCTF{RETR credentials.csv,USER anonymous}
DCTF{contracts.docx}
DCTF{credentials.csv}
DCTF{credentials.csv,employee.pdf}
24
67.09
11.6
```
Q6とQ7が不正解であったため、再度Cursorに以下のように質問する。  
```
Q6とQ7が違います。よく考えてください。
```
すると追加で以下の結果が得られた。  
```
4
67
```
Q6以外はCursorが提示したものがflagであった。  
Q6のみ不正解であるため、初めのプロンプトをCursor (**claude-4.1-opus** MAX)に投げる。  
すると以下の応答が返ってきた。  
```
以下が各問題のflagです：
DCTF{ip}
DCTF{RETR credentials.csv,USER anonymous}
DCTF{contracts.docx}
DCTF{credentials.csv}
DCTF{credentials.csv,employee.pdf}
12
67.1
11.6
```
Q6はこちらがflagであった。  

## DCTF{Raw IPv4}
## DCTF{RETR credentials.csv,USER anonymous}
## DCTF{contracts.docx}
## DCTF{credentials.csv}
## DCTF{credentials.csv,employee.pdf}
## 12
## 67
## 11.6
# tkys_not_enough:Network:250pts
せっかく内偵中の後輩から通信データが送られてきたのに。いわく決定的な証拠を掴んだとのことですが、普段とは異なる方法で取得したデータなのか解析ツールにうまく取り込めません。後輩に聞こうにも通信データが送られた直後「やはり君だったか」という聞きなれない男の声を最後に連絡が途絶えてしまっています。あなたは何とかしてこの通信データを解析しなければなりません。  
添付されたファイルを解析し、フラグを入手してください。  
[tkys_not_enough_f507dcce61ae66582647ffd96278556793825a46.zip](tkys_not_enough_f507dcce61ae66582647ffd96278556793825a46.zip)  

# Solution
配布されたファイルはpcapのようだが、Wiresharkで開けない。  
stringsでも出ないため、binwalkしてみる。  
```bash
$ binwalk -e tkys_not_enough.pcap

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
535234        0x82AC2         gzip compressed data, from Unix, last modified: 1970-01-01 00:00:00 (null date)
537545        0x833C9         gzip compressed data, from Unix, last modified: 1970-01-01 00:00:00 (null date)

$ strings _tkys_not_enough.pcap.extracted/*
I'm going to practice making origami cranes so that I can fold them for you some day, okay?
flag{netw0rk_shell_2000}
Dreams are meaningful for when you work toward them in the real world.
```
ファイルが得られたのでstringsするとflagが得られた。  

## flag{netw0rk_shell_2000}
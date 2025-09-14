# east-grandma:Forensics:50pts
Investigate the wants of the most expensive club on the east coast.  

[camashadefortza.jpg](camashadefortza.jpg)  

---

Q1. What is the flag? (Points: 50)  
ctf{sha256}  

# Solution
jpgファイルだけが渡される。  
ジャンルがForensicsということもあり、何かが含まれていそうだ。  
```bash
$ binwalk --dd='.*' camashadefortza.jpg

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, JFIF standard 1.01
206006        0x324B6         7-zip archive data, version 0.4

```
binwalkすると7-zipが含まれていた。  
展開を試みるとパスワード付きのようなので、rockyou.txtでクラックを行う。  
```bash
$ ./7z2john.pl 324B6 > hash.txt
ATTENTION: the hashes might contain sensitive encrypted data. Be careful when sharing or posting these hashes
$ cat hash.txt
324B6:$7z$0$19$0$$16$0cb3ababf964175a592ec4dec8ee51f7$1105515733$144$130$8c9fc34a5ad969da07afcc12b237e17edba92378483eb8739cfb7fae7864c188b2826d8bd8d21cf242040e5cff4a3aec74dcdd80690a30bcc3317b0da6a2559a67e6e3c0c1ab8f9937277854008079c15061e7d27ae0b5b002a435cebf896513736426a7ce7e1ba72300ebf281cc953441f292d83c7970a6e9829e59b2ec1db24f9e8b71466a3bb305af0fcad0e3858c
$ ./john --format=7z hash.txt --wordlist=rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (7z, 7-Zip archive encryption [SHA256 256/256 AVX2 8x AES])
Cost 1 (iteration count) is 524288 for all loaded hashes
Cost 2 (padding size) is 14 for all loaded hashes
Cost 3 (compression type) is 0 for all loaded hashes
Cost 4 (data length) is 130 for all loaded hashes
Will run 16 OpenMP threads
Note: Passwords longer than 28 rejected
Press 'q' or Ctrl-C to abort, 'h' for help, almost any other key for status
passwordpassword (324B6)
1g 0:00:04:46 DONE (2025-09-14 00:04) 0.003485g/s 177.1p/s 177.1c/s 177.1C/s passwordpassword..magnavox
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```
パスワードは`passwordpassword`のようだ。  
展開するとbeaches.001が出てくるのでstringsしてgrepする。  
```bash
$ file beaches.001
beaches.001: DOS/MBR boot sector, code offset 0x52+2, OEM-ID "NTFS    ", sectors/cluster 8, Media descriptor 0xf8, sectors/track 63, heads 255, hidden sectors 2048, dos < 4.0 BootSector (0), FAT (1Y bit by descriptor); NTFS, sectors/track 63, physical drive 0x80, sectors 20479, $MFT start cluster 853, $MFTMirror start cluster 2, bytes/RecordSegment 2^(-1*246), clusters/index block 1, serial number 014844777844759fe; contains bootstrap BOOTMGR
$ strings beaches.001 | grep ctf
Tip de muzica: Rock Alternativ .... ce gluma ... muzica de vitamina ctf{sha256(vamonos)}
```
`ctf{sha256(vamonos)}`がヒットしたので、文字列`vamonos`のsha256sumを指定された形式にするとflagとなった。  

## ctf{44ad656b71865ac4ad2e485cfbce17423e0aa0bcd9bcdf2d98a1cb1048cf4f0e}
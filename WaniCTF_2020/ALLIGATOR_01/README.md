# ALLIGATOR_01:Forensics:pts
ワニ博士のPCでは，悪意のあるプロセスが実行されているみたいです。  
取得したメモリダンプから、”evil.exe”が実行された日時を報告してください。  
(注意: スペースはすべて半角のアンダースコアにしてください)  
example: FLAG{1234-56-78_99:99:99_UTC+0000}  
問題ファイル: [ALLIGATOR.zip](https://mega.nz/file/dHZWkTzA#9a-yHID2Fg_upTaVmYKhO_3-gu7Q0JbLiw-HSfarQyU) (ミラー: [ALLIGATOR.zip](https://drive.google.com/file/d/1yb6Ojbl7xkgRYU-4DgNi-0iJWT6jO2uW/view?usp=sharing))  
推奨ツール: [volatility](https://github.com/volatilityfoundation/volatility)  

# Solution
ALLIGATOR.zipをダウンロードできる。  
※ファイルサイズの問題でALLIGATOR.zipを分割している(`cat ALLIGATOR.zip-?? > ALLIGATOR.zip`で戻せる)。  
```text
03615eb6105da1c7445350147dc2540c4ba2be5f  ALLIGATOR.zip
420a8b26adda90620792331c90f6fb8499825c6c  ALLIGATOR.zip-00
085e32b327ff6dfb48f86af402e401aa04a0ba6a  ALLIGATOR.zip-01
ea059741c7624ce8d1639a5d3b22bc3dc414ecda  ALLIGATOR.zip-02
c2464435909c16ca3fde8df8eeb254c6fba300d3  ALLIGATOR.zip-03
39e1343dcdba13584bf6cafc7ee053d2a9482ab9  ALLIGATOR.zip-04
79cd366013f24771c6762eb37f54e1342671d992  ALLIGATOR.zip-05
a33887b9899095ff70e484eb149236edd6e158f7  ALLIGATOR.zip-06
```
unzipするとrawファイルが出てくる。  
```bash
$ unzip ALLIGATOR.zip
Archive:  ALLIGATOR.zip
  inflating: ALLIGATOR.raw
```
問題文通りvolatilityを使用する。  
pstreeを見ればよい。  
```bash
$ volatility -f ALLIGATOR.raw imageinfo
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : Win7SP1x86_23418, Win7SP0x86, Win7SP1x86
                     AS Layer1 : IA32PagedMemoryPae (Kernel AS)
                     AS Layer2 : FileAddressSpace (/ALLIGATOR.raw)
                      PAE type : PAE
                           DTB : 0x185000L
                          KDBG : 0x82754de8L
          Number of Processors : 1
     Image Type (Service Pack) : 1
                KPCR for CPU 0 : 0x80b96000L
             KUSER_SHARED_DATA : 0xffdf0000L
           Image date and time : 2020-10-26 03:04:49 UTC+0000
     Image local date and time : 2020-10-25 20:04:49 -0700
$ volatility -f ALLIGATOR.raw --profile=Win7SP1x86_23418 pstree | grep evil.exe
Volatility Foundation Volatility Framework 2.6
. 0x84dd6b28:evil.exe                                3632   2964      1     21 2020-10-26 03:01:55 UTC+0000
```
2020-10-26 03:01:55 UTC+0000らしいので形式通りに整形する。  

## FLAG{2020-10-26_03:01:55_UTC+0000}
# かに座:Misc - Water elements:14pts
仲間はずれを探せ  
[cancer.zip](cancer.zip)  

Hint  
zipファイルをダウンロードして展開すると、13個のファイルが中に含まれているのがわかります。  
1個だけ仲間はずれがあるようです。実はこの問題にはいろんな見方があるんですが、一番簡単なのは更新日時とか…  
Hint  
仲間はずれのファイルの開き方なんですが、まずファイルの種類を調べる必要があります。  
どうやら今回は普通にメモ帳で開けるみたいです。開いてみてください。 よく見ると…  

# Solution
zipが渡され、仲間はずれを探せと言われる。  
解凍し、ファイル形式を調べる。  
```bash
$ unzip cancer.zip
~~~
$ file cancer/*
cancer/0961db32a59b8a83c1996498f9d1d80e: pcapng capture file - version 1.0
cancer/397cbf6db9d7ae6906ae420aedc5346c: pcapng capture file - version 1.0
cancer/44ca0844398b2d010d8cd4a31ddb023d: pcapng capture file - version 1.0
cancer/4de447a391e32baeb5a52c55aa14467b: pcapng capture file - version 1.0
cancer/550eadb88a230018bf043d1b6ad15863: pcapng capture file - version 1.0
cancer/635cbc8a5dc1a528c3b5cb9eecdc1086: pcapng capture file - version 1.0
cancer/7463543d784aa59ca86359a50ef58c8e: pcapng capture file - version 1.0
cancer/766cc4dd4d5005652e8514e3513683f8: pcapng capture file - version 1.0
cancer/7c70e2cb2b4a13c4590f6b15c30385fd: pcapng capture file - version 1.0
cancer/a0678bcea04dbd6852c219062ab2bb3c: pcapng capture file - version 1.0
cancer/b9c94e8a87e3647c5a0fa4ff358ecc65: pcapng capture file - version 1.0
cancer/f0525aafa095ed2665d03681537a70ea: Unicode text, UTF-8 text
cancer/f8a5c386478fa64f118056b82acc31d2: pcapng capture file - version 1.0
```
一つだけtxtなのでcatする。  
```bash
$ cat cancer/f0525aafa095ed2665d03681537a70ea
Open in Notepad.Open in Notepad.Open in Notepad.Open in Notepad.
~~~
Open in Notepad.Open in Notepad.Open in Notepad.Open in Notepad.
nazotokiCTF{イイワケ}
```
flagである`イイワケ`が書かれていた。  

## イイワケ
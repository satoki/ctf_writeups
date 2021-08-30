# Host:30:pts
あなたはある通信を保存したファイルを受け取りました。添付されたファイルを解析し、通信先の Web サーバのホスト名を特定してください。  
フラグはホスト名をフラグ形式で答えてください。例えばホスト名が `host.example.com` であった場合、フラグは `flag{host.example.com}` となります。  
[host_d52855b24d8814504c54538f37af0355aa79214f.zip](host_d52855b24d8814504c54538f37af0355aa79214f.zip)  

# Solution
Wiresharkげー。  
開くのが面倒なので、stringsで見る。  
```bash
$ strings host.pcap | grep Host
Host: ctf.setodanote.net
```
指定された形式に整形するとflagとなった。  

## flag{ctf.setodanote.net}
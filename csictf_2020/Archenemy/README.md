# Archenemy:Forensics:368pts
John likes Arch Linux. What is he hiding?  
[arched.png](arched.png)  

# Solution
arched.pngが渡される。  
stringsしても何も出ないようだ。  
steghideするとflag.zipが出てきたが、パスワードがかかっている。  
```bash
$ steghide extract -sf arched.png
Enter passphrase:
wrote extracted data to "flag.zip".
$ unzip flag.zip
Archive:  flag.zip
[flag.zip] meme.jpg password:
```
[ZIP file password removal](https://passwordrecovery.io/zip-file-password-removal/)でパスワードが`kathmandu`とわかる。  
総当たりを試してもよい。  
解凍するとmeme.jpgが出てきた。  
![meme.jpg](meme.jpg)  
フラグが書かれている。  

## csictf{1_h0pe_y0u_don't_s33_m3_here}
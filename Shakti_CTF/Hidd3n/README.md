# Hidd3n:Steganography:100pts
Seems like there is something hidden in this image. Can you find it out?  
[image.jpg](image.jpg)  

# Solution
image.jpgが配布される。  
![image.jpg](image.jpg)  
jpgなので、exiftoolで見てみる。  
```bash
$ exiftool image.jpg
ExifTool Version Number         : 10.80
File Name                       : image.jpg
Directory                       : .
File Size                       : 44 kB
File Modification Date/Time     : 2020:12:05 18:27:02+09:00
File Access Date/Time           : 2020:12:05 18:27:39+09:00
File Inode Change Date/Time     : 2020:12:05 18:27:02+09:00
File Permissions                : rwxrwxrwx
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Resolution Unit                 : None
X Resolution                    : 1
Y Resolution                    : 1
Comment                         : cGFzc3BocmFzZT1qdTV0ZmluZG0z
Image Width                     : 800
Image Height                    : 600
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:4:4 (1 1)
Image Size                      : 800x600
Megapixels                      : 0.480
```
コメントに`cGFzc3BocmFzZT1qdTV0ZmluZG0z`が入っている。  
base64デコードすると`passphrase=ju5tfindm3`になる。  
passphraseが出てきたので`ju5tfindm3`でsteghideする。  
```bash
$ steghide extract -sf image.jpg
Enter passphrase:
wrote extracted data to "flag.txt".
$ cat flag.txt
"In engineering, the point is to get the job done, and people are happy to help. You should be generous with credit, and you should be happy to help others." Who am I?

Here is your flag: shaktictf{G00d!_b3st_0f_luck_f0r_th3_n3xt_chall3nge}
```
flagが得られた。  

## shaktictf{G00d!_b3st_0f_luck_f0r_th3_n3xt_chall3nge}
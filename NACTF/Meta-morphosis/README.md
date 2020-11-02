# Meta-morphosis:Forensics:75pts
Mikey really likes Metamorphosis by Franz Kafka, so much so that he sent this meme to the class.  
[meme-3.jpg](meme-3.jpg)  

# Solution
画像が渡されるが、jpgである。  
exifを見てみる。  
```bash
$ ls
meme-3.jpg
$ exiftool meme-3.jpg
ExifTool Version Number         : 10.80
File Name                       : meme-3.jpg
Directory                       : .
File Size                       : 52 kB
File Modification Date/Time     : 2020:11:01 11:11:11+09:00
File Access Date/Time           : 2020:11:01 11:11:11+09:00
File Inode Change Date/Time     : 2020:11:01 11:11:11+09:00
File Permissions                : rwxrwxrwx
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
X Resolution                    : 1
Y Resolution                    : 1
Exif Byte Order                 : Big-endian (Motorola, MM)
Resolution Unit                 : None
Artist                          : nactf{m3ta_m3ta_m3ta_d3f4j}
Y Cb Cr Positioning             : Centered
Image Width                     : 500
Image Height                    : 461
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:4:4 (1 1)
Image Size                      : 500x461
Megapixels                      : 0.231
```
Artistにflagが隠されていた。  

## nactf{m3ta_m3ta_m3ta_d3f4j}
# User Guide:PEGASUS:10pts
While bored during the holidays because the Wi-Fi at your family's house is infuriatingly slow, you decided to go poking around through the garage. You come across a dusty cardboard box containing a very unusual computerized device along with some program cartridges. The first cartridge is labelled "PEGASUS User Guide". Why not pop it in, power the machine up, and see what happens?  

=====  

PEGASUS User Guide program file:  
- [PEGASUS_User_Guide.peg](PEGASUS_User_Guide.peg)  

Core PEGASUS files:  
- [libpegasus_ear.so](libpegasus_ear.so)  
- [runpeg](runpeg)  
- [submitpeg](submitpeg)  

How to run a PEGASUS file:  
runpeg <file.peg> [--debug] [--verbose] [--trace]  

# Solution
謎の問題だが言われたとおりに実行してみる。  
```bash
$ ./runpeg PEGASUS_User_Guide.peg
sun{1n_4_w0rld_0f_pur3_d3lir1ati0n}
```
flagが出てきた。  

## sun{1n_4_w0rld_0f_pur3_d3lir1ati0n}
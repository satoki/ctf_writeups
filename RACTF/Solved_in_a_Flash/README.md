# Solved in a Flash:Reversing / Pwn:100pts
Someone found a weird microcontroller sitting on the desk when they walked into the office this morning. They reckoned it was a challenge, so made an image of flash and sent it your way. Good luck!  
[flash.bin](flash.bin)  

# Solution
flash.binが何のファイルかわからないがstringsは便利だった。  
```bash
$ file flash.bin
flash.bin: data
$ strings flash.bin | grep ractf
ractf{Fl4shDump5Ar3VeryFun!!}
```

## ractf{Fl4shDump5Ar3VeryFun!!}
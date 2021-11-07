# partition01:Forensics:177pts
新しくUSBを買ったのでたくさんパーティションを作ってみました！  
[for-partition01.zip](for-partition01.zip)  

# Solution
zipを解凍すると、tar.gzがありその中に1.9GB程のimgがおさまっていた。  
binwalkゲーを行う。  
```bash
$ binwalk -e partition.img

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
1048576       0x100000        Linux EXT filesystem, blocks count: 65536, image size: 67108864, rev 1.0, ext4 filesystem data, UUID=30bcce20-7041-4d80-ace4-6463453e453e, volume name "WANI"
135265280     0x80FFC00       Linux EXT filesystem, blocks count: 65536, image size: 67108864, rev 1.0, ext4 filesystem data, UUID=30bcce20-7041-4d80-ace4-6463453e453e, volume name "WANI"
269484032     0x10100000      Linux EXT filesystem, blocks count: 65536, image size: 67108864, rev 1.0, ext4 filesystem data, UUID=5223fb56-44b6-4085-85cd-a906894e894e, volume name "CTF"
403700736     0x180FFC00      Linux EXT filesystem, blocks count: 65536, image size: 67108864, rev 1.0, ext4 filesystem data, UUID=5223fb56-44b6-4085-85cd-a906894e894e, volume name "CTF"
537919488     0x20100000      Linux EXT filesystem, blocks count: 65536, image size: 67108864, rev 1.0, ext4 filesystem data, UUID=b1ebbc76-a6e5-4a94-af8e-f66264326432, volume name "FLAG{GPT03}"
672136192     0x280FFC00      Linux EXT filesystem, blocks count: 65536, image size: 67108864, rev 1.0, ext4 filesystem data, UUID=b1ebbc76-a6e5-4a94-af8e-f66264326432, volume name "FLAG{GPT03}"
806354944     0x30100000      Linux EXT filesystem, blocks count: 65536, image size: 67108864, rev 1.0, ext4 filesystem data, UUID=3cdcf545-49ea-4365-a694-11644d784d78, volume name "NANI"
940571648     0x380FFC00      Linux EXT filesystem, blocks count: 65536, image size: 67108864, rev 1.0, ext4 filesystem data, UUID=3cdcf545-49ea-4365-a694-11644d784d78, volume name "NANI"
1074790400    0x40100000      Linux EXT filesystem, blocks count: 65536, image size: 67108864, rev 1.0, ext4 filesystem data, UUID=2ccf7158-e3e1-4a67-bc1e-550a93af93af, volume name "FLAG01"
1209007104    0x480FFC00      Linux EXT filesystem, blocks count: 65536, image size: 67108864, rev 1.0, ext4 filesystem data, UUID=2ccf7158-e3e1-4a67-bc1e-550a93af93af, volume name "FLAG01"
1343225856    0x50100000      Linux EXT filesystem, blocks count: 65536, image size: 67108864, rev 1.0, ext4 filesystem data, UUID=38753979-6907-4e4e-a120-3ee45d055d05, volume name "FAKE"
1477442560    0x580FFC00      Linux EXT filesystem, blocks count: 65536, image size: 67108864, rev 1.0, ext4 filesystem data, UUID=38753979-6907-4e4e-a120-3ee45d055d05, volume name "FAKE"
1611661312    0x60100000      Linux EXT filesystem, blocks count: 65536, image size: 67108864, rev 1.0, ext4 filesystem data, UUID=c6ecae8e-a097-474d-a718-b567e77ee77e, volume name "FLAG02"
1745878016    0x680FFC00      Linux EXT filesystem, blocks count: 65536, image size: 67108864, rev 1.0, ext4 filesystem data, UUID=c6ecae8e-a097-474d-a718-b567e77ee77e, volume name "FLAG02"
1880096768    0x70100000      Linux EXT filesystem, blocks count: 32507, image size: 33287168, rev 1.0, ext4 filesystem data, UUID=68eb051c-18fd-4106-bf21-5bc497fb97fb, volume name "DUMMY"
```
ボリュームの名前がflagだった。  

## FLAG{GPT03}
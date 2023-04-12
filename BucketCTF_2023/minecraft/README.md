# minecraft:MISC:200pts
I just started playing minecraft for my computer science class and forgot to remove a sign with my password before exiting the world. Could you please check what my password is.  

[bucketctfMC.mcworld](bucketctfMC.mcworld)  

# Solution
minecraftのワールドファイルが配布されている。  
ゲームで読み込む前に、binwalkでファイルを分解してgrep、stringsにかける。  
```bash
$ binwalk -e bucketctfMC.mcworld

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             Zip archive data, at least v3.0 to extract, compressed size: 214414, uncompressed size: 1218435, name: db/000003.log
214477        0x345CD         Zip archive data, at least v3.0 to extract, compressed size: 15, uncompressed size: 16, name: db/CURRENT
214552        0x34618         Zip archive data, at least v3.0 to extract, compressed size: 52, uncompressed size: 50, name: db/MANIFEST-000002
214672        0x34690         Zip archive data, at least v3.0 to extract, compressed size: 1536, uncompressed size: 2732, name: level.dat
216267        0x34CCB         Zip archive data, at least v3.0 to extract, compressed size: 1535, uncompressed size: 2732, name: level.dat_old
217865        0x35309         Zip archive data, at least v3.0 to extract, compressed size: 10, uncompressed size: 8, name: levelname.txt
217938        0x35352         Zip archive data, at least v3.0 to extract, compressed size: 23737, uncompressed size: 23923, name: world_icon.jpeg
242153        0x3B1E9         End of Zip archive, footer length: 22

$ cd _bucketctfMC.mcworld.extracted/
$ grep -r bucket{
grep: db/000003.log: binary file matches
$ strings db/000003.log | grep bucket{
bucket{1L0V3MIN
bucket{1L0V3MIN
bucket{1L0V3MIN
$ strings db/000003.log | grep bucket{ -3
PersistFormatting
SignTextColor
Text&
bucket{1L0V3MIN
3CRAFT_1c330e9
105f1}
TextIgnoreLegacyBugResolved
--
PersistFormatting
SignTextColor
Text&
bucket{1L0V3MIN
3CRAFT_1c330e9
105f1}
TextIgnoreLegacyBugResolved
--
PersistFormatting
SignTextColor
Text&
bucket{1L0V3MIN
3CRAFT_1c330e9
105f1}
TextIgnoreLegacyBugResolved
```
改行されているが、flagが得られた。  

## bucket{1L0V3MIN3CRAFT_1c330e9105f1}
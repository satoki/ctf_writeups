# Invisible:Steganography:50pts
One of our engineer got some clues regarding a recent attack in the city, using her knowledge on networking. Can you connect the dots and help us?  
Flag Format : shaktictf{STRING}  
[file.jpg](file.jpg)　　　　[file.txt](file.txt)  

# Solution
file.jpgとfile.txtが配布される。  
jpgが怪しいが`Nothing here :(`の文字列しか見つからない。  
txtをメモ帳で開いても`Nothing here :(`と書かれているのみだった。  
しかしtxtをよく見ると不自然な空白が存在していることに気付いた。  
「steganography tabs spaces」でググるとstegsnowなるものがあるらしい。  
```bash
$ stegsnow file.txt
_z/Q}达QG}Ez/E}}}}}达
$ stegsnow -C file.txt
.- -- .---- ...- .---- ... .. -... .-.. ...-- -. ----- .--
```
圧縮されているためCオプションが必要らしい。  
モールス信号らしき文字列が隠されていた。  
[Morse Code Translator](https://morsecode.world/international/translator.html)で復号すると`AM1V1SIBL3N0W`となった。  
これを指定された形式に整形するとflagとなった。  
jpgを使っていない。  

## shaktictf{AM1V1SIBL3N0W}
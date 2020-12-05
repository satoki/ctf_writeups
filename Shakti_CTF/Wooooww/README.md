# Wooooww:Misc:100pts
Some terrorists implanted a spy microphone in our office and tried sending some important project details to their country. The ENIAC programmers caught that and we need your help to extract the secret message.  
Flag format : shaktictf{STRING}  
[findit.mp3](findit.mp3)  

# Solution
findit.mp3が配られる。  
波形などには何も隠されていないようだ。  
聞いてみると様々な種類の音が録音されている。  
途中でよく聞くモールス信号が流れてくるので、カットして[Morse Code Adaptive Audio Decoder](https://morsecode.world/international/decoder/audio-decoder-adaptive.html)でデコードしてみる。  
`LOLM0RS3I5FUNN`とデコードされた。  
指定された通りの形式に整形するとflagとなった。  

## shaktictf{LOLM0RS3I5FUNN}
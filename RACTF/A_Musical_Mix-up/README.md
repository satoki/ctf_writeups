# A Musical Mix-up:Steg / Forensics:200pts
One of our guys found a strange midi file lying around on our servers. We think there might be some hidden data in it. See if you can help us out!  
[challenge.mid](challenge.mid)  

# Solution
challenge.midを開いてみても、ピアノ曲が流れるだけである。  
stringsしてみる。  
```bash
$ strings -n 1 challenge.mid | tr -d "\n"
MThdMTrkMXYQye?[]!Hr_HLa_LHc_HLt_LHf_HL{_LHf_HL5_LH0_HLc_LH1_HL3_LHt_HLy_LH__HLl_LG3_GLv_LGe_GLloLG_oGH5_HHtoHG3oGHg_HL!_LH}_HLr_LHa_HLc_LHt_HLf_LH{_HLf_LG5_GL0_LGc_GL1oLG3oGHt_HHyoHG_oGHl?HH3oHLv_LLeoLHloHQH_oHG5_GGtoG@3o@EgoEG!oGH}oHJroJLa_LLcoLHtoHQHfoHG{_GGfoGE5oEaG0_GHc?HQG1oGH3_HHtoHGyoGQG_oGEl_EE3oEGvoGQEeoELl_LJ_oJH5oHQEtoEL3_LJg_JH!?HaL}OLLrOLEaEaLcOLLtOLEf?EM{?MaLfOLL5OLE0EHcoHL1_LL3oLHtoHQHyoHG__GGloG@3o@EvoEGeoGHloHJ_oJL5_LLtoLH3oHQHgoHG!_GG}oGEroEaGa_GHc?HQGtoGHf_HH{oHGfoGQG5oGE0_EEcoEG1oGQE3oELt_LJyoJH_oHQEloEL3_LJv_JHe?HaLlOLL_OLE5EaLtOLL3OLEg?EM!?MaL}OLLrOLEaEOcOOtwOMfwML{wLJfwJL5?LQL0oLJc?JQJ1oJH3oHGtoGEyoEG_oGHloHJ3oJLvoLMeoMOlOO_wOM5wMLtwLJ3wJLg?LQL!oLJ}?JQJroJHaoHGcoGEtoEGfoGH{oHJfoJL5oLM0oMOc?OH1T3?HTGtSyGSH_TlHTAH3Tv?HTGeSlGSH__HL5_LHt_HL3_LHg_HL!_LH}_HLr_LGa_GLc_LGt_GLfoLG{oGHf_HH5oHG0oGHc_HL1_LH3_HLt_LQHy_HL__LQ Hl_HL3_LHv_HLe_LGl_GL__LG5_GLtoLG3oGQRHg_HH!oHG}oGHr?H/MTrkY!@~0a@@=07c<t?7<-f@@=-4{9f?49(540@@=(48c;1?8;)35t@@=)59y<_?9<0l@@=073<v?7<-e@@=-4l9_?49(54t@@=(483;g?8;)!5}@@=)59r<a?9<$c@@=$4t7f?47!{-f@@=!-45?4(0@@=(4c81?48)3@@=)5t9y?59$_@@=$4l73?47!v-e@@=!-4l9_?49(5@@=(4t83?48)g@@=)5!9}?59$r@@=$4a7c?47!t-f@@=!-4{9f?49(5@@=(408c?48)1@@=)539t?590y@@=07_<l?7<-3@@=-4v9e?49(l4_@@=(485;t?8;)35g@@=)59!<}?9<0r@@=07a<c?7<-t@@=-4f9{?49(f45@@=(480;c?8;)153@@=)59t<y?9<@$_@@=$4l73?47!v-e@@=!-4l?4(_@@=(458t?48)3@@=)5g9!?59$}@@=$4r7a?47!c-t@@=!-4f9{?49(f@@=(4580?48)c@@=)5193?59$t@@=$4y7_?47!l-3@@=!-4v9e?49(l@@=(4_85?48)t@@=)539g?590!@@=07}<r?7<-a@@=-4c9t?49(f4{@@=(48f;5?8;)05c@@=)591<3?9<0t@@=07y<_?7<-l@@=-439v?49(e4l@@=(48_;5?8;)t53@@=)59g<!?9<0}@@=07r<a?7<-c@@=-4t9f?49({4f@@=(485;0?8;)c51@@=)593<t?9<0y@@=07_<l?7<-3@@=-4v9e?49(l4_@@=(485;t?8;)35g@@=)59!<}?9<0r@@=07a<c?7<-t@@=-4f9{?49(f45@@=(480;c?8;)153@@=)59t<y?9<0_@@=07l<3?7<-v@@=-4e9l?49(_45@@=(48t;3?8;)g5!@@=)58}<r?8<0a@@=07c<t?7<-f@@=-4{9f?49(540@@=(48c;1?8;)35t@@=)59y<_?9<0l@@=073<v?7<-e@@=-4l9_?49(54t@@=(483;g?8;)!5}@@=)59r<a?9<@/
```
一番上にractfらしきものがあるので抽出する。  
```bash
$ strings -n 1 challenge.mid | tr -d "HLGo_\n"
MThdMTrkMXYQye?[]!ractf{f50c13tyl3vel5t3g!}ractf{f50c13tyl?3velQ5t@3@EgE!}
~~~
```
ractf{f50c13tyl3vel5t3g!}が得られた。  
_が間に入っていることに注意。  

## ractf{f50c13ty_l3vel_5t3g!}
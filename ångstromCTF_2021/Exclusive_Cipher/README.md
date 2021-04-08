# Exclusive Cipher:Crypto:40pts
Clam decided to return to classic cryptography and revisit the XOR cipher! Here's some hex encoded ciphertext:  
`ae27eb3a148c3cf031079921ea3315cd27eb7d02882bf724169921eb3a469920e07d0b883bf63c018869a5090e8868e331078a68ec2e468c2bf13b1d9a20ea0208882de12e398c2df60211852deb021f823dda35079b2dda25099f35ab7d218227e17d0a982bee7d098368f13503cd27f135039f68e62f1f9d3cea7c`  
The key is 5 bytes long and the flag is somewhere in the message.  

# Solution
ただのXOR暗号のようだ。  
鍵が5バイトと教えられている。  
flagが中に含まれているらしいので、actf{の5バイトでXORするとどこかに鍵が出てくる。  
以下のactfxor.pyで行う。  
```python:actfxor.py
c = 0xae27eb3a148c3cf031079921ea3315cd27eb7d02882bf724169921eb3a469920e07d0b883bf63c018869a5090e8868e331078a68ec2e468c2bf13b1d9a20ea0208882de12e398c2df60211852deb021f823dda35079b2dda25099f35ab7d218227e17d0a982bee7d098368f13503cd27f135039f68e62f1f9d3cea7c
c = bin(c)[2:]
c = [c[i: i+40] for i in range(0, len(c), 40)]

a = "0110000101100011011101000110011001111011" #actf{

keys = []
for i in c:
    keys.append(int(a, 2) ^ int(i, 2))

flags = []
for i in keys:
    tmp = []
    for j in c:
        flag = i ^ int(j, 2)
        flag = flag.to_bytes((flag.bit_length() + 7) // 8, byteorder='big')
        try:
            flag = flag.decode()
        except:
            break
        tmp.append(flag)
    flags.append("".join(tmp))

for i in flags:
    if "actf{" in i:
        print(i)
```
実行する。  
```bash
$ python3 actfxor.py
actf{CxomhVeuozct!mGohxyVetf)Vd!dGi`nG-:UaG,|mhE,sr)CongrUdu^gGi~rVCii^~Jit^pMyEihTiEyfPq4!NMc~!eWoq!fL,nilcnilP,ysp
Cxomhactf{t~ndi xo*~etssjt~om:td*wedrk}e6!^re7gf{g7hy:atulawnUtereyEarrUmhroUcob^b{vr^rurj/*]oxe*vutj*un7ub xubr7bxc
Veuozt~ndiactf{5eu(lpiiqxacuo(ab~(epyhiop+;\`p*}dir*r{(tionsbbtWfpo{WtohW}ouWqzD`icoDpggw5(Oze(d`ip(g{*o`m5eo`mg*xzq
ct!m xo*~5eu(lactf{$oh?o5et!?5dfr$i'x$-:w$,|*~&,s5? on d6duq$i~5@ iih)itf.yE.~7iE>p3q4fX.c~fs4oqfp/,n.zacn.z3,y4f
Gohxyetssjpiiqx$oh?oactf{pihx+phc?fasu~la!&Kca `sjc ol+ecrypshi@eaeblTeeu@|leh@rkuYwjreYgdv}(?Lkob?gqcm?dj rwn$orwnv emr
Vetf)t~om:acuo(5et!?pihx+actf{ab!6pyi`<p+:U3p*|m:r*sr{ting bbu^5po~rtoi^,}ot^"zEi:coEy4gw4!ze~!7`iq!4{*ni>5eni>g*ys"
Vd!dtd*wab~(e5dfrphc?fab!6actf{pxb'qp*1~p+w*wr+x56the mbc~xpnu5Itnba}noz~N.wcnN>ygv?fQzdufz`hzfy{+e.s5de.sg+r4o
Gi`nedrk}pyhio$i'xasu~lpyi`<pxb'qactf{a1'Sta0ak}c0nt<essagsxhXrauctCeutXkluiXekeXo}ruXsvm)'[kc'pqsl'sj0soy$soyv0due
G-:Uae6!^rp+;\`$-:wa!&Kcp+:U3p*1~a1'Stactf{ab2^rcb=A3e! Ths*;m}a'0ALe''mdl':mjk7Zrr'J|v?zTk-0q!?|jb Zv$- Zvvb7@j
G,|mhe7gf{p*}di$,|*~a `sjp*|m:p+w*wa0ak}ab2^ractf{cc{y:e flas+}Uta&vyEe&aUml&|Uck6Mb{r&Mruv><*]k,v*vq y*ujcfb$,fbvcqxc
E,sr)g7hy:r*r{(&,s5?c ol+r*sr{r+x56c0nt<cb=A3cc{y:actf{g is q+rJ5c&yfg&nJ,n&sJ"i6B}:p&Bm4t>35i,y57s v54hci}>&,i}>tc~g"
Congratulations on decrypting the message! The flag is actf{who_needs_aes_when_you_have_xor}. Good luck on the other cry
Udu^gwnUtbbtWf6duqshi@ebbu^5bc~xsxhXrs*;m}s+}Utq+rJ5who_nactf{snJJwnhfb~nufly~DQt`nDAzdv5Rydychpzx+oQp6doQpd+xKl
Gi~rVereyEpo{W$i~5@aeblTpo~rpnu5IauctCa'0ALa&vyEc&yfeeds_snJJactf{eccJSlc~J]ksO}ErcOmKv{>5ckit5Hqe{5Kj&d}A$id}Av&sg]
Cii^~arrUmtohW iiheeu@|toi^,tnbaeutXke''mde&aUmg&nJ,aes_wwnhfbeccJSactf{hcifuosXQmvcXAcr{)Koic`uelcn&sQi isQir&dKu
Jit^phroUc}ouWq)itfleh@r}ot^"}noluiXel':mjl&|Ucn&sJ"hen_y~nufllc~J]hcifuactf{fsEQccEAm{{4Efi~n|eqmg&nQg)inQg{&yK{
MyEihob^b{zD`i.yE.~kuYwjzEi:z~N.wkeXo}k7Zrk6Mb{i6B}:ou_hay~DQtksO}EosXQmfsEQcactf{xstvu|k.]ayO.v{u@.u`6_f.y_f|6H|c
TiEyfvr^rucoDpg7iE>preYgdcoEy4cnN>yruXsr'J|r&Mrup&Bm4ve_xo`nDAzrcOmKvcXAccEAmxstvuactf{e{>SxiO>xbe@>{y&_vq7i_vqe&Hlm
Pq4!Nrj/*]gw5(O3q4fXv}(?Lgw4!gv?fQvm)'[v?zTv><*]t>35r}. Gdv5Rv{>5cr{)K{{4E|k.]e{>Sactf{|q>fPf}1fS}>..Y3q..Ya>94E
Mc~!eoxe*vze(d.c~fskob?gze~!7zdufzkc'pk-0k,v*vi,y57ood lydykit5Hoic`fi~nayO.vxiO>x|q>fPactf{{o{fx`,d.r.cd.r|,s4n
Woq!futj*u`ip(g4oqfpqcm?d`iq!4`hzfyqsl'sq!?|q y*us v54uck ochpzqe{5Kuelc|eqm{u@.ube@>{f}1fS{o{fxactf{z k.q4ok.qf |4m
L,niln7ub{*o`m/,n.zj rwn{*ni>{+e.sj0soyjb Zvjcfbhci}>n thex+oQpj&d}An&sQig&nQg`6_fy&_vq}>..Y`,d.rz k.qactf{/,tf{}cc|g
cnil xub5eo`macn.z$orwn5eni>5de.s$soy$- Zv$,fb&,i}> othe6doQp$id}A isQi)inQg.y_f7i_vq3q..Y.cd.r4ok.q/,tf{actf{3,c|g
P,yspr7bxcg*xzq3,y4fv emrg*ys"g+r4ov0duevb7@jvcqxctc~g"r cryd+xKlv&sg]r&dKu{&yK{|6H|ce&Hlma>94E|,s4nf |4m}cc|g3,c|gactf{
```
真ん中あたりにflagがあった。  

## actf{who_needs_aes_when_you_have_xor}
# MITRE:OSINT:100pts
識別子があることを知っておくことは共通の認識をもつために必要なことでしょう。ですが、すべての識別子を覚える必要はないと思います。そういう理由で私はこの課題に必要性を感じません。そう説得したが教官は首を縦に振ってはくれなかった。そして、私はこれからこの文字列を解読しなければならない。  
`T1495T1152T1155T1144 T1130T1518 flag{T1170T1118T1099T1496T1212_T1531T1080T1127T1020T1081T1208_T1112T1098T1199T1159T1183T1220_T1111T1147T1220}`  
フラグに英字が含まれる場合はすべて大文字で答えてください。  

# Solution
TXXXXの形式のものが複数並んでいる。  
MITREのテクニックIDであるようだ。  
それぞれの頭文字をとってくると予測する。  
```text
T1495:mitre_t1495_firmware_corruption
T1152:mitre_t1152_launchctl
T1155:mitre_t1155_applescript
T1144:mitre_t1144_gatekeeper_bypass

T1130:mitre_t1130_install_root_certificate
T1518:mitre_t1518_software_discovery
~~~
```
`flag is`からなるようだ。  
[ここ](https://docs.vmware.com/jp/VMware-Carbon-Black-Cloud/services/carbon-black-cloud-user-guide/GUID-0B68199D-6411-45D1-AE0D-2AB9B7A28513.html)を見ると楽に解読できる。  
一文字ずつ拾うとflagとなった。  

## flag{MITRE_ATTACK_MATLIX_THX}
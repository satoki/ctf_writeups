import math
from Crypto.Util.number import inverse
from Crypto.Util.number import long_to_bytes

n=133957491909745071464818932891535809774039075882486614948793786706389844163167535932401761676665761652470189326864929940531781069869721371517782821535706577114286987515166157005227505921885357696815641758531922874502352782124743577760141307924730988128098174961618373787528649748605481871055458498670887761203
e=65537
c1=35405298533157007859395141814145254094484385088710533905385734792407576252003080929963085838327711405177354982539867453717921912839308282313390558033140654288445877937672625603540090399691469218188262950682485682814224928528948502206046863184746747265896306678488587444125143233443450049838709221084210200357
c2=23394879596667385465597018769822552384439114548016006879565586102300995936951562766011707923675690015217418498865916391314367448706185724546566348496812451258316472754407976794025546555423254676274654957362894171995220230464953432393865332807738040967281350952790472772600745096787761443699676372681208295288
c3=54869102748428770635192859184579301467475982074831093316564134451063250935340131274147041633101346896954483059058671502582914428555153910133076778016989842641074276293354765141522703887273042367333036465503084165682591308676428523152462442280924054400997210800504726635778588407034149919869556306659386868798

p = math.gcd(n, c2 + c3)
q = n // p

print(p)
print(q)

phi = (p-1) * (q-1)
d = inverse(e, phi)
m = pow(c1, d, n)
print(long_to_bytes(m))
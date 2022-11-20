from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes, GCD

def enc(p_text):
  N=p*q
  c_text=pow(p_text,e,N)
  #cipher_text=plain_text^e mod N
  print('cipher text:',c_text)
  print('p:',p)
  print('q:',q)
  print('e:',e)

e = 65537
p = getPrime(100)
q = getPrime(100)

#e:public key
#p,q: prime number

plain=b'UECTF{SECRET}'
plain=bytes_to_long(plain)
#bytes_to_long:bytes -> number
#long_to_bytes:number->bytes
enc(plain)

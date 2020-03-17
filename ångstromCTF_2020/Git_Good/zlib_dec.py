import zlib

f1 = open("3c94c0b90a897f246f0f32dec3f5fd3e40abb5")
f2 = open("75d678f209da09fff763cd297a6ed8dd77bb35")
print(zlib.decompress(f1.read()))
print(zlib.decompress(f2.read()))
f1.close()
f2.close()
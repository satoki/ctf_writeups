import zlib

f = open("3f47cbcb3ad8e946d0aad59259bdb1bc9e63f2")
wf = open("image_blob", mode='wb')
wf.write(zlib.decompress(f.read()))
f.close()
wf.close()
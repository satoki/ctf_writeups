import math
import base64

text = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_} !?#\n"

flag = "xm4s{"

key = "paswd"
blocksize = len(key)
initial_vector = "abcde"

b = 1

while True:
    if (b == 1) and (not "}" in flag):
        b = 0
    else:
        print(flag.encode())
        break
    for i1 in text:
        if b == 1:
            break
        print(i1)
        for i2 in text:
            if b == 1:
                break
            for i3 in text:
                if b == 1:
                    break
                for i4 in text:
                    if b == 1:
                        break
                    for i5 in text:
                        _flag = flag
                        _flag += "{}{}{}{}{}".format(i1, i2, i3, i4, i5)
                        if len(_flag)%blocksize != 0:
                            _flag += '#' * (blocksize - len(_flag)%blocksize)
                        encrypted_flag = ""
                        last_enc = initial_vector
                        for i in range(0,len(_flag),blocksize):
                            asciicode = [ord(j) for j in _flag[i:i+blocksize]]
                            chain = [asciicode[j] ^ ord(last_enc[j]) for j in range(blocksize)]
                            enc = [chain[j] ^ ord(key[j]) for j in range(blocksize)]
                            enc = ''.join([chr(j) for j in enc])
                            encrypted_flag += enc
                            last_enc = enc
                        if encrypted_flag.encode("utf-8") in base64.b64decode("aW4kYHpQUDt+dUVuC0tSamoWX0RjexFBT307HzwI"):
                            print(_flag)
                            flag = _flag
                            b = 1
                            break
                        #print(encrypted_flag.encode("utf-8"))
                        #print(base64.b64decode("aW4kYHpQUDt+dUVuC0tSamoWX0RjexFBT307HzwI"))
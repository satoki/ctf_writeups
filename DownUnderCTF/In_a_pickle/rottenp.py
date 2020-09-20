import pickle
import string

text = pickle.load(open('data', mode='rb'))

print(text)
print("-"*40)

for i in range(1,24):
    try:
        print(chr(text[i]),end="")
    except:
        print(text[i],end="")
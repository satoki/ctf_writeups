import random, time

i = input(">")
s = round(time.time() / 100, 5)
print("[{}]".format(s))

while True:
    s = round(s - 0.00001, 5)
    random.seed(s)
    #print(s)
    if str(random.randint(1, 100000000)) == i:
        print(random.randint(1, 100000000))
        print(random.randint(1, 100000000))
        break
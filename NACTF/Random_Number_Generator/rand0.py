try:
    with open("flag.txt", "r") as fin:
        flag = fin.read()
except:
    print("Problem is misconfigured - ping us on discord if this is happening on the shell server")
    exit()

import random, time
random.seed(round(time.time() / 100, 5))

print("Welcome to Dr. J's Random Number Generator!")
print("[r] Print a new random number")
print("[g] Guess the next two random numbers and receive the flag!")
print("[q] Quit")


while True:
    inp = input("\n> ")
    if inp == "r":
        print(random.randint(1, 100000000))
    elif inp == "g":
        print("Guess the next two random numbers for a flag!\nGood luck!\nEnter your first guess:")
        if input("> ") == str(random.randint(1, 100000000)):
            print("Wow, lucky guess... You won't be able to guess right a second time\nEnter your second guess:")
            if input("> ") == str(random.randint(1, 100000000)):
                print("What? You must have psychic powers... Well here's your flag: ")
                print(flag)
                break
            else:
                print("That's incorrect. Get out of here!")
                break
        else:
            print("That's incorrect. Get out of here!")
            break
    elif inp == "q":
        print("Goodbye!")
        break
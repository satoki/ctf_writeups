import random

flag = b"FAKE{this_is_a_fake_flag}"


def main():
    number = random.randint(0, 500000)
    print("find a number")
    for i in range(20):
        print("challenge", i)
        client_challenge = int(input("input:"))
        if client_challenge == number:
            print("correct!!!")
            print(flag)
            exit()
        elif client_challenge < number:
            print("too small")
            print("try again!")
        else:
            print("too big")
            print("try again!")
    print("You've failed too many times")


if __name__ == "__main__":
    main()

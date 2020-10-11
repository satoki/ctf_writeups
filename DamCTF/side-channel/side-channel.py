#!/usr/bin/env python3

import secrets
import codecs
import time

# init with dummy data
password = 'asdfzxcv'
sample_password = 'qwerasdf'


# print flag! call this!
def cat_flag():
    with open("./flag", 'rt') as f:
        print(f.read())

# initialize password
def init_password():
    global password
    global sample_password
    # seems super secure, right?
    password = "%08x" % secrets.randbits(32)
    sample_password = "%08x" % secrets.randbits(32)

# convert hex char to a number
# '0' = 0, 'f' = 15, '9' = 9...
def charactor_position_in_hex(c):
    string = "0123456789abcdef"
    return string.find(c[0])

# the function that matters..
def guess_password(s):
    print("Password guessing %s" % s)
    typed_password = ''
    correct_password = True
    for i in range(len(password)):
        user_guess = input("Guess character at position password[%d] = %s?\n" \
                % (i, typed_password))
        typed_password += user_guess
        if user_guess != password[i]:
            # we will punish the users for supplying wrong char..
            time.sleep(0.3 * charactor_position_in_hex(password[i]))
            correct_password = False

    # to get the flag, please supply all 8 correct characters for the password..
    if correct_password:
        cat_flag()

    return correct_password

# main function!
def main():
    init_password()
    print("Can you tell me what my password is?")
    print("We randomly generated 8 hexadecimal digit password (e.g., %s)" % sample_password)
    print("so please guess the password character by character.")
    print("You have only 2 chances to test your guess...")
    guess_password("Trial 1")
    if not guess_password("Trial 2"):
        print("My password was %s" % password)

if __name__ == '__main__':
    main()

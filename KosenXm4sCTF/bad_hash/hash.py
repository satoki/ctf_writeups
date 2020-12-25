#!/bin/python3

def hash(base):
    xor_sum = 0
    mod_sum = 0
    for c in base.encode():
        xor_sum ^= c
        mod_sum += c
        mod_sum %= 100
   
    return (xor_sum, mod_sum)

with open("./password.txt") as f:
    answer = f.read()

ans_x, ans_m = hash(answer)
print(f'ans_x {ans_x}, ans_m {ans_m}')

user_input = input()
if 10 <= len(user_input):
    print("too long...")

inp_x, inp_m = hash(user_input)
print(f'inp_x {inp_x}, inp_m {inp_m}')

if ans_x == inp_x and ans_m == inp_m:
    print("You hava a password!!")
    with open('./flag.txt') as f:
        print(f.read())




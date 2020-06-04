#!/usr/bin/env python2.7

try:
    print("Welcome to my calculator!")
    print("You can add, subtract, multiply and divide some numbers")

    print("")

    first = int(input("First number: "))
    second = int(input("Second number: "))

    operation = str(raw_input("Operation (+ - * /): "))

    if first != 1 or second != 1:
        print("")
        print("Sorry, only the number 1 is supported")

    if first == 1 and second == 1 and operation == "+":
        print("1 + 1 = 2")
    if first == 1 and second == 1 and operation == "-":
        print("1 - 1 = 0")
    if first == 1 and second == 1 and operation == "*":
        print("1 * 1 = 1")
    if first == 1 and second == 1 and operation == "/":
        print("1 / 1 = 1")
    else:
        print(first + second)
except ValueError:
    pass

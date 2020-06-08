import math

x = 0.0
z = 0.0
flag_x = 10000000000000.0
flag_z = 10000000000000.0
print("Your player is at 0,0")
print("The flag is at 10000000000000, 10000000000000")
print("Enter your next position in the form x,y")
print("You can move a maximum of 10 metres at a time")
for _ in range(100):
    print(f"Current position: {x}, {z}")
    try:
        move = input("Enter next position(maximum distance of 10): ").split(",")
        new_x = float(move[0])
        new_z = float(move[1])
    except Exception:
        continue
    diff_x = new_x - x
    diff_z = new_z - z
    dist = math.sqrt(diff_x ** 2 + diff_z ** 2)
    if dist > 10:
        print("You moved too far")
    else:
        x = new_x
        z = new_z
    if x == 10000000000000 and z == 10000000000000:
        print("ractf{#####################}")
        break


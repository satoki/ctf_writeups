#!/usr/bin/env python3

import pty

print(
    """  _________________________
     ||   ||     ||   ||
     ||   ||, , ,||   ||
     ||  (||/|/(\\||/  ||
     ||  ||| _'_`|||  ||
     ||   || o o ||   ||
     ||  (||  - `||)  ||
     ||   ||  =  ||   ||
     ||   ||\\___/||   ||
     ||___||) , (||___||
    /||---||-\\_/-||---||\\
   / ||--_||_____||_--|| \\
  (_(||)-| SP1337 |-(||)_)
          --------
"""
)

print("Hello prisoner, welcome to jail.")
print("Don't get any ideas, there is no easy way out!")
while 1:
    try:
        input(": ")
    except KeyboardInterrupt:
        print()
        continue
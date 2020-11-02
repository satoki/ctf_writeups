import socket

# Open socket to interact with challenge server
s = socket.socket()

# address = "challenges.ctfd.io", port = 30267
s.connect(("challenges.ctfd.io",30267))

# Receive initial info
info = s.recv(4096).decode("utf-8")
print(info)

# Choose challenge
s.send(b'2\n')
response = s.recv(4096).decode("utf-8")
print(response)

# Get veggies 🥬🥕🌽🍆🥦🥒🥑🍄
veggies = response.split("\n\n")[1].split(', ')
print (veggies)

# Send the robot instructions
s.send('1 2 3\n'.encode('utf-8'))
response = s.recv(4096).decode("utf-8")

print(response)


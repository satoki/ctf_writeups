import socket

host = "2020.redpwnc.tf"
port = 31284
text = "11001101101100110000111001111111011" + "X"*259 + "1111101"
# "flag{" + X + "}"
text = list(text)

try:
    for i in range(1, 300):
        print("[{}]".format(i))
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        client.recv(256)
        client.send(("{}\n".format(i)).encode('utf-8'))
        client.recv(256)
        client.send(("{}\n".format(i + 1)).encode('utf-8'))
        response = client.recv(1024)
        response = response.decode('utf-8')
        response = response.replace("Ciphertext: ", "")
        for j in range(len(text)):
            if j % (i + 1) == 0:
                text[j] = (str(int(response[j]) ^ 1))
        #print(response)
        #print("".join(text))
    text = "".join(text)
    print(text)
    for i in range(0, len(text), 7):
        print(chr(int(text[i: i+7], 2)), end="")
    print()
except:
    print("\n" + "".join(text))
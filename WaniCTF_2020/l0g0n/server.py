from hashlib import pbkdf2_hmac
import os

from Crypto.Cipher import AES

from secret import flag, psk


class AES_CFB8:
    def __init__(self, key):
        self.block_size = 16
        self.cipher = AES.new(key, AES.MODE_ECB)

    def encrypt(self, plaintext: bytes, iv=bytes(16)):
        iv_plaintext = iv + plaintext
        ciphertext = bytearray()

        for i in range(len(plaintext)):
            X = self.cipher.encrypt(iv_plaintext[i : i + self.block_size])[0]
            Y = plaintext[i]
            ciphertext.append(X ^ Y)
        return bytes(ciphertext)


def key_derivation_function(x):
    dk = pbkdf2_hmac("sha256", x, os.urandom(16), 100000)
    return dk


def main():
    while True:
        client_challenge = input("Challenge (hex) > ")
        client_challenge = bytes.fromhex(client_challenge)

        server_challenge = os.urandom(8)
        print(f"Server challenge: {server_challenge.hex()}")

        session_key = key_derivation_function(psk + client_challenge + server_challenge)

        client_credential = input("Credential (hex) > ")
        client_credential = bytes.fromhex(client_credential)

        cipher = AES_CFB8(session_key)
        server_credential = cipher.encrypt(client_challenge)
        if client_credential == server_credential:
            print(f"OK! {flag}")
        else:
            print("Authentication Failed... 🥺")


if __name__ == "__main__":
    main()

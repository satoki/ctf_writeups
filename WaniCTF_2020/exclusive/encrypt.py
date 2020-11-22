key = "REDACTED"
flag = "FAKE{this_is_fake_flag}"

assert len(key) == len(flag) == 57
assert flag.startswith("FLAG{") and flag.endswith("}")
assert key[0:3] * 19 == key


def encrypt(s1, s2):
    assert len(s1) == len(s2)

    result = ""
    for c1, c2 in zip(s1, s2):
        result += chr(ord(c1) ^ ord(c2))
    return result


ciphertext = encrypt(flag, key)
print(ciphertext, end="")

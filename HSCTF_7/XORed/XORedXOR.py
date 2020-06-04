Key1 = 0x5dcec311ab1a88ff66b69ef46d4aba1aee814fe00a4342055c146533
Key13 = 0x9a13ea39f27a12000e083a860f1bd26e4a126e68965cc48bee3fa11b
Key235 = 0x557ce6335808f3b812ce31c7230ddea9fb32bbaeaf8f0d4a540b4f05
Key145 = 0x7b33428eb14e4b54f2f4a3acaeab1c2733e4ab6bebc68436177128eb
Key34 = 0x996e59a867c171397fc8342b5f9a61d90bda51403ff6326303cb865a
FlagKey12345 = 0x306d34c5b6dda0f53c7a0f5a2ce4596cfea5ecb676169dd7d5931139

Key3 = Key1 ^ Key13
Key4 = Key3 ^ Key34
Key5 = Key1 ^ Key4 ^ Key145
Key2 = Key3 ^ Key5 ^ Key235

Flag = FlagKey12345 ^ Key1 ^ Key2 ^ Key3 ^ Key4 ^ Key5

print(hex(Flag))
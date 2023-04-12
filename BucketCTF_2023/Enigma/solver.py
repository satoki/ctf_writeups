from enigma.machine import EnigmaMachine

for a in range(1, 26):
    for b in range(1, 26):
        for c in range(1, 26):
            machine = EnigmaMachine.from_key_sheet(
                rotors="I II III",
                reflector="B",
                ring_settings=[a, b, c],
                plugboard_settings="AT BS DE FM IR KN LZ OW PV XY"
            )
            plaintext = machine.process_text("rvvrwdxyficctevo").lower()
            if "bucket" in plaintext:
                print(plaintext)
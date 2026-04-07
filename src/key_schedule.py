from .sbox import SBOX, RCON

def key_expansion(key: bytes):
    assert len(key) == 16

    w = []

    # First 4 words from key
    for i in range(4):
        w.append(list(key[4*i:4*i+4]))

    # Generate remaining words
    for i in range(4, 44):
        temp = w[i-1][:]

        if i % 4 == 0:
            # RotWord
            temp = temp[1:] + temp[:1]

            # SubWord
            temp = [SBOX[b] for b in temp]

            # XOR with RCON
            temp[0] ^= RCON[i//4 - 1]

        w.append([w[i-4][j] ^ temp[j] for j in range(4)])

    # Convert into round keys
    round_keys = []
    for r in range(11):
        rk = [[w[r*4+c][row] for c in range(4)] for row in range(4)]
        round_keys.append(rk)

    return round_keys
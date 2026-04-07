def xtime(a):
    return ((a << 1) ^ 0x1B) & 0xFF if (a & 0x80) else (a << 1) & 0xFF

def gf_mul(a, b):
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a
        a = xtime(a)
        b >>= 1
    return result
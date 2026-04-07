from .sbox import SBOX, INV_SBOX
from .gf256 import gf_mul


# SubBytes
def sub_bytes(state):
    return [[SBOX[state[r][c]] for c in range(4)] for r in range(4)]


def inv_sub_bytes(state):
    return [[INV_SBOX[state[r][c]] for c in range(4)] for r in range(4)]


# ShiftRows
def shift_rows(state):
    return [
        [state[0][0], state[0][1], state[0][2], state[0][3]],
        [state[1][1], state[1][2], state[1][3], state[1][0]],
        [state[2][2], state[2][3], state[2][0], state[2][1]],
        [state[3][3], state[3][0], state[3][1], state[3][2]],
    ]


def inv_shift_rows(state):
    return [
        [state[0][0], state[0][1], state[0][2], state[0][3]],
        [state[1][3], state[1][0], state[1][1], state[1][2]],
        [state[2][2], state[2][3], state[2][0], state[2][1]],
        [state[3][1], state[3][2], state[3][3], state[3][0]],
    ]


# MixColumns
def mix_columns(state):
    result = [[0]*4 for _ in range(4)]
    for c in range(4):
        col = [state[r][c] for r in range(4)]
        result[0][c] = gf_mul(0x02,col[0])^gf_mul(0x03,col[1])^col[2]^col[3]
        result[1][c] = col[0]^gf_mul(0x02,col[1])^gf_mul(0x03,col[2])^col[3]
        result[2][c] = col[0]^col[1]^gf_mul(0x02,col[2])^gf_mul(0x03,col[3])
        result[3][c] = gf_mul(0x03,col[0])^col[1]^col[2]^gf_mul(0x02,col[3])
    return result


def inv_mix_columns(state):
    result = [[0]*4 for _ in range(4)]
    for c in range(4):
        col = [state[r][c] for r in range(4)]
        result[0][c] = gf_mul(0x0e,col[0])^gf_mul(0x0b,col[1])^gf_mul(0x0d,col[2])^gf_mul(0x09,col[3])
        result[1][c] = gf_mul(0x09,col[0])^gf_mul(0x0e,col[1])^gf_mul(0x0b,col[2])^gf_mul(0x0d,col[3])
        result[2][c] = gf_mul(0x0d,col[0])^gf_mul(0x09,col[1])^gf_mul(0x0e,col[2])^gf_mul(0x0b,col[3])
        result[3][c] = gf_mul(0x0b,col[0])^gf_mul(0x0d,col[1])^gf_mul(0x09,col[2])^gf_mul(0x0e,col[3])
    return result


# AddRoundKey
def add_round_key(state, round_key):
    return [[state[r][c] ^ round_key[r][c] for c in range(4)] for r in range(4)]
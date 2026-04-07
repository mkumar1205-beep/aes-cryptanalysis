from .aes_core import (
    sub_bytes,
    shift_rows,
    mix_columns,
    add_round_key
)
from .key_schedule import key_expansion

def bytes_to_state(data: bytes):
    return [[data[r + 4*c] for c in range(4)] for r in range(4)]


def state_to_bytes(state) -> bytes:
    return bytes([state[r][c] for c in range(4) for r in range(4)])


def aes_encrypt(plaintext: bytes, key: bytes, num_rounds: int = 10) -> bytes:
    """AES encryption with configurable rounds"""
    
    round_keys = key_expansion(key)
    state = bytes_to_state(plaintext)

    # Initial round
    state = add_round_key(state, round_keys[0])

    # Main rounds
    for r in range(1, num_rounds):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, round_keys[r])

    # Final round (no MixColumns)
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, round_keys[num_rounds])

    return state_to_bytes(state)
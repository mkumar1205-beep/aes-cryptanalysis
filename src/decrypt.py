from .aes_core import (
    inv_shift_rows,
    inv_sub_bytes,
    inv_mix_columns,
    add_round_key
)
from .key_schedule import key_expansion
from .encrypt import bytes_to_state, state_to_bytes

def aes_decrypt(ciphertext: bytes, key: bytes, num_rounds: int = 10) -> bytes:
    round_keys = key_expansion(key)
    state = bytes_to_state(ciphertext)
    state = add_round_key(state, round_keys[num_rounds])

    for r in range(num_rounds - 1, 0, -1):
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state = add_round_key(state, round_keys[r])
        state = inv_mix_columns(state)

    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    state = add_round_key(state, round_keys[0])

    return state_to_bytes(state)
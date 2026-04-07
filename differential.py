import os
import math
from src.encrypt import aes_encrypt

def compute_difference(a: bytes, b: bytes) -> bytes:
    return bytes([x ^ y for x, y in zip(a, b)])


def differential_analysis(key: bytes, num_rounds: int = 2, num_pairs: int = 500):
    print(f"\n{'='*55}")
    print(f" Differential Analysis — {num_rounds}-Round AES")
    print(f"{'='*55}")

    diff_distribution = {}

    for _ in range(num_pairs):
        p1 = os.urandom(16)
        delta_in = bytes([0x01] + [0x00]*15)
        p2 = bytes([p1[i] ^ delta_in[i] for i in range(16)])
        c1 = aes_encrypt(p1, key, num_rounds)
        c2 = aes_encrypt(p2, key, num_rounds)
        delta_out = compute_difference(c1, c2)
        key_out = delta_out[:2]
        diff_distribution[key_out] = diff_distribution.get(key_out, 0) + 1

    print(f"  Input difference:  0x01 (first byte)")
    print(f"  Pairs tested:      {num_pairs}")
    print(f"  Unique outputs:    {len(diff_distribution)}")

    top = sorted(diff_distribution.items(), key=lambda x: -x[1])[:5]

    print(f"\n  Top output differences:")
    for diff, count in top:
        pct = 100 * count / num_pairs
        print(f"  {diff.hex()} → {count} ({pct:.1f}%)")

    total = sum(diff_distribution.values())
    entropy = -sum((c/total)*math.log2(c/total) for c in diff_distribution.values())
    max_entropy = math.log2(256**2)

    print(f"\n  Entropy: {entropy:.2f} / {max_entropy:.2f}")
    print(f"  Uniformity: {100*entropy/max_entropy:.1f}%")

    if entropy/max_entropy > 0.95:
        print("Strong diffusion(secure)")
    else:
        print("Differential bias detected!")

    print(f"{'='*55}\n")
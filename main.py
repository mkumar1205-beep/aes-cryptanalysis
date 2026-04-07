from src.encrypt import aes_encrypt
from src.decrypt import aes_decrypt
from cryptanalysis.differential import differential_analysis

def print_block(label, data: bytes):
    print(f"{label}: {data.hex().upper()}")

def main():
    print("=" * 60)
    print(" AES-128 Implementation + Cryptanalysis Demo ")
    print("=" * 60)

    # NIST test vector (standard correctness test)
    key = bytes.fromhex("000102030405060708090A0B0C0D0E0F")
    plaintext = bytes.fromhex("00112233445566778899AABBCCDDEEFF")
    expected_cipher = bytes.fromhex("69C4E0D86A7B0430D8CDB78070B4C55A")

    print("\n[1] AES Encryption Test (NIST Vector)")
    print_block("Key       ", key)
    print_block("Plaintext ", plaintext)

    ciphertext = aes_encrypt(plaintext, key)
    print_block("Ciphertext (computed)", ciphertext)
    print_block("Ciphertext (expected)", expected_cipher)

    if ciphertext == expected_cipher:
        print("Encryption correct!")
    else:
        print("Encryption mismatch!")

    # Decryption test
    print("\n[2] AES Decryption Test")
    decrypted = aes_decrypt(ciphertext, key)
    print_block("Decrypted", decrypted)

    if decrypted == plaintext:
        print("Decryption correct!")
    else:
        print("Decryption failed!")

    # Differential cryptanalysis
    print("\n[3] Differential Cryptanalysis Demo")

    for rounds in [1, 2, 3, 4]:
        differential_analysis(key, num_rounds=rounds, num_pairs=300)

    print("=" * 60)
    print(" Demo Complete ")
    print("=" * 60)


if __name__ == "__main__":
    main()
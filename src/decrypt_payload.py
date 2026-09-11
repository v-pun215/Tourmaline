#!/usr/bin/env python3
"""
Tourmaline Payload Decryptor & Anti-Sandbox Time-Lock Bypass

This tool demonstrates the O(1) algebraic key recovery that bypasses
the malware's 100,000,000-iteration sandbox evasion delay loop.
"""

import os
import sys
import struct

def decrypt_payload(dxf_path="samples/QGBdu.dxf", output_path="decrypted_payload.py"):
    if not os.path.exists(dxf_path):
        # fallback to local search
        if os.path.exists("../samples/QGBdu.dxf"):
            dxf_path = "../samples/QGBdu.dxf"
        else:
            print(f"[-] Error: Could not find {dxf_path}")
            return False

    with open(dxf_path, "rb") as f:
        ciphertext = f.read()

    print(f"[+] Loaded ciphertext ({len(ciphertext)} bytes) from {dxf_path}")

    # hardcoded 29-byte key suffix
    key_suffix = bytes.fromhex("2b0cffe07b06ac25793b3f00cfaa2dd5881c2d6378165247539dbbdaeb")
    # expected plaintext prefix ("g1 = lambda l6, ")
    known_plaintext = bytes.fromhex("6731203d206c616d626461206c362c20")

    # O(1) Instant Key Recovery
    # since ciphertext[i] ^ key[i] == plaintext[i], key[:4] = ciphertext[:4] ^ plaintext[:4]
    key_prefix = bytes(ciphertext[i] ^ known_plaintext[i] for i in range(4))
    full_key = key_prefix + key_suffix
    key_len = len(full_key)

    recovered_n = struct.unpack(">I", key_prefix)[0]
    print(f"[+] Recovered countdown integer _n : {recovered_n} (0x{key_prefix.hex()})")
    print(f"[+] Full 33-byte XOR key          : {full_key.hex()}")

    # decrypt
    decrypted = bytes(ciphertext[i] ^ full_key[i % key_len] for i in range(len(ciphertext)))

    with open(output_path, "wb") as f:
        f.write(decrypted)

    print(f"[+] Successfully decrypted payload ({len(decrypted)} bytes) -> {output_path}")
    return True

if __name__ == "__main__":
    in_file = sys.argv[1] if len(sys.argv) > 1 else "samples/QGBdu.dxf"
    out_file = sys.argv[2] if len(sys.argv) > 2 else "decrypted_payload.py"
    decrypt_payload(in_file, out_file)

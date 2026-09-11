# Tourmaline
I recently stumbled upon a piece of cleverly designed malware that calls itself "Torumaline".

This README is very kindly written by Claude as I was super busy with exams at the time of this repository's inception. 

Exploiting and decrypting this malware took a huge chunk of my time from math prep!

Read the [blogpost!](https://vihaan.dev/inside-tourmaline)

> **FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY**  
> All samples are provided for malware analysis and defensive research. Do not execute outside a sandboxed, air-gapped environment.

---

## Overview

**Tourmaline** (`Tourmaline.exe`) is a sophisticated, multi-stage Windows infostealer/backdoor distributed via a **ClickFix campaign** - a fake Cloudflare "Verify you are human" browser popup that tricks users into manually running a malicious command or installer.

The binary is a custom-built **Inno Setup 6.7.0 (Revision 2, 64-bit offsets)** installer that bundles a full Python 3.11 runtime and two stages of obfuscated Python payload. It establishes a persistent backdoor with:

- **DNS tunneling** C2 over UDP port 53 (masquerading as `microsoft.com` queries)
- **Ethereum blockchain dead-drop** for C2 IP distribution (Sepolia testnet)
- **ChaCha20-encrypted** task execution channel
- **ECDSA-signed** commands to prevent sinkholing
- **Anti-sandbox time-lock** (100M iteration countdown, bypassable in O(1))

---

## Repository Structure

```
tourmaline/
├── README.md                  # This file
├── LICENSE                    # Research use license
├── .gitignore
│
├── src/                       # Extracted & deobfuscated source code
│   ├── stage1_loader.py       # Stage 1: Original obfuscated XOR time-lock loader (main.py)
│   ├── stage2_backdoor.py     # Stage 2: Deobfuscated core backdoor (from QGBdu.dxf)
│   └── decrypt_payload.py     # Utility: O(1) payload key recovery & decryption
│
├── iocs/                      # Indicators of Compromise
│   ├── indicators.json        # Structured IOC data (IPs, hashes, domains, registry)
│   ├── indicators.csv         # Flat CSV for SIEM import
│   └── rules.yar              # YARA detection rules
│
└── samples/                   # Malware samples (password-protected)
    ├── README.md              # Sample archive instructions
    ├── Tourmaline_sample.zip  # Password: infected - contains Tourmaline.exe
    └── QGBdu.dxf             # Raw encrypted Stage 2 payload blob
```

---

## Infection Vector

The malware is distributed via **ClickFix** - a social engineering technique where a compromised or attacker-controlled website overlays a fake Cloudflare CAPTCHA or browser verification page. The overlay instructs the victim to:

1. Press `Win+R`
2. Paste a command (copied to clipboard by the page's JavaScript)
3. Press Enter

The pasted command downloads and silently executes `Tourmaline.exe`. The installer runs `/VERYSILENT /SUPPRESSMSGBOXES /NORESTART`.

---

## Binary Format

| Property | Value |
|---|---|
| **File name** | `Tourmaline.exe` |
| **Size** | 11,341,339 bytes (~10.8 MB) |
| **MD5** | `b74ac808dea2de31caf024310694ef0c` |
| **SHA256** | `c9b390b3b7148f549df86503858d52e030b2b5e78fed0bc525ded5927f9265d6` |
| **Format** | Inno Setup 6.7.0 Unicode (Revision 2, 64-bit offsets) |
| **PE type** | 32-bit PE, 11 sections |
| **Overlay size** | 10,447,387 bytes |
| **Inno magic offset** | 0xD9864 (890,148 bytes) |
| **App name** | `Tourmaline` |
| **App version** | `2.63.519` |
| **App GUID** | `{2C25872D-85FC-44C7-9B16-844E39E50A44}` |
| **Install path** | `{commonappdata}\Tourmaline` |
| **Bundled runtime** | Python 3.11 (full embed) |
| **Payload files** | 36 files in solid LZMA2 stream |

> **Note:** Stock `innoextract 1.9` cannot extract this binary — it only supports Revision 1. Revision 2 uses 64-bit offsets and requires custom parsing (see `src/decrypt_payload.py`).

---

## Execution Flow

```
Tourmaline.exe
│
├─ Inno Setup installer runs silently
│   ├─ Extracts Python 3.11 runtime to %APPDATA%\Tourmaline\
│   ├─ Extracts main.py (Stage 1 loader)
│   ├─ Extracts QGBdu.dxf (encrypted Stage 2 blob)
│   ├─ Kills any existing pythonw.exe instances
│   └─ Registers persistence (Task Scheduler / registry)
│       └─ Name: "TourmalineUpdate" / "Hardware monitoring service"
│
├─ Stage 1: main.py (XOR Time-Lock Loader)
│   ├─ Counts _n from 99,999,999 → 0 (anti-sandbox delay ~hours on slow VMs)
│   ├─ At each _n, constructs 33-byte XOR key: struct.pack('>I', _n) + hardcoded_suffix
│   ├─ Tests key against known plaintext header of QGBdu.dxf
│   └─ On match: decrypts QGBdu.dxf entirely and exec()s the result
│       └─ O(1) bypass: known-plaintext attack on first 4 bytes (see below)
│
└─ Stage 2: QGBdu.dxf → Python backdoor
    ├─ Reads MachineGuid from HKLM\SOFTWARE\Microsoft\Cryptography
    ├─ Derives mutex Global\Tourmaline_<hash>
    ├─ Resolves C2 IP via Ethereum dead-drop (Sepolia testnet)
    ├─ Establishes DNS tunnel to C2
    └─ Poll-execute loop: fetches tasks, exec()s Python, returns output
```

---

## Stage 1 — Anti-Sandbox Time-Lock (O(1) Bypass)

The loader (`main.py`) uses a countdown from `99,999,999` to find the XOR decryption key. On a real machine this completes in seconds (because `_n` starts high and the true value is near `14,511,188`). In a sandbox with a short time limit, the loop never completes.

**Key structure:**
```
full_key = struct.pack('>I', _n) + bytes.fromhex('2b0cffe07b06ac25793b3f00cfaa2dd5881c2d6378165247539dbbdaeb')
```

Since we know the first 16 bytes of the plaintext (`g1 = lambda l6, `), we can recover `_n` instantly via known-plaintext XOR attack:

```python
key_prefix = bytes(ciphertext[i] ^ known_plaintext[i] for i in range(4))
# Result: key_prefix = 00dd6c54 → _n = 14,511,188
```

Use `src/decrypt_payload.py` to reproduce this.

---

## Stage 2 — Core Backdoor Architecture

### Configuration (Hardcoded)

| Parameter | Value |
|---|---|
| **C2 IP** | `158.94.211.185` |
| **C2 Port** | `53` (UDP) |
| **Protocol** | Custom DNS-over-UDP tunnel |
| **Spoofed domain** | `microsoft.com` |
| **ChaCha20 key** | `36f555c87f71581f57d83576c88193fdc00a0173f741a3e198e2d7abdc9cda59` |
| **Blockchain contract** | `0x2d7a04cca0c34005f58393f30ac725e25f19e5f5` (Sepolia) |
| **ECDSA pubkey** | `MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEt17l3rGHHR9sYdHEvV8S+JRRCUHQQveSadlGk04xM/8WClDf/67Tyritt2+T18SY8n0xv1TKKl0AgnNFuboEEQ==` |
| **Service name** | `SystemService` / `TourmalineUpdate` |
| **Mutex** | `Global\Tourmaline_<MachineGuid-hash>` |

### Blockchain Dead-Drop (C2 Resilience)

The malware calls an Ethereum smart contract on the **Sepolia testnet** to retrieve the active C2 IP address. This means the attacker can change the C2 IP at any time by updating the contract — traditional IP blocklist-based C2 disruption is ineffective.

```
Contract : 0x2d7a04cca0c34005f58393f30ac725e25f19e5f5
Selector : 0xeb9fd6fe
Network  : Ethereum Sepolia (chainId 11155111)
RPC      : https://ethereum-sepolia-rpc.publicnode.com
Result   : ChaCha20-encrypted blob containing current C2 IP
```

The returned data is decrypted with the hardcoded ChaCha20 key to reveal the live C2 address. At time of analysis, this resolved to **`158.94.211.185`** (verified via live RPC call).

### DNS Tunnel (C2 Communication)

All C2 traffic is sent as **raw UDP DNS queries** directly to the C2 IP on port 53. Queries are structured as `<encoded_data>.microsoft.com`, bypassing DNS-based filtering and appearing as legitimate Windows telemetry.

- **Custom implementation**: Does not use Python's `socket.getaddrinfo` or any DNS library
- **Opcode obfuscation**: Each packet has a random XOR byte applied to the DNS opcode field
- **Encoding**: Task data is base-encoded into DNS label format

### Task Execution Engine

The backdoor implements an arbitrary Python `exec()` engine. Tasks are:
1. Fetched from C2 via DNS tunnel
2. ChaCha20-decrypted
3. ECDSA-signature-verified (prevents sinkhole injection)
4. `exec()`'d in a persistent namespace with output capture
5. Results returned to C2

**Supported task types:** Python exec, file upload/download, shell command, self-update.

---

## Indicators of Compromise (IOCs)

### Network

| Type | Value |
|---|---|
| C2 IP | `158.94.211.185` |
| C2 Port | `53/UDP` |
| Spoofed Domain | `*.microsoft.com` (custom UDP, not real DNS) |
| Ethereum RPC | `https://ethereum-sepolia-rpc.publicnode.com` |
| Smart Contract | `0x2d7a04cca0c34005f58393f30ac725e25f19e5f5` |

### File Hashes

| File | SHA256 |
|---|---|
| `Tourmaline.exe` | `c9b390b3b7148f549df86503858d52e030b2b5e78fed0bc525ded5927f9265d6` |
| `Tourmaline.exe` (MD5) | `b74ac808dea2de31caf024310694ef0c` |

### Registry / Persistence

| Key | Value |
|---|---|
| `HKLM\SOFTWARE\Microsoft\Cryptography\MachineGuid` | Read for victim fingerprinting |
| `%APPDATA%\Tourmaline\` | Installation directory |
| Task Scheduler | `TourmalineUpdate` |
| Service display name | `Hardware monitoring service` |
| Mutex | `Global\Tourmaline_<hash>` |

---

## YARA Rules

See [`iocs/rules.yar`](iocs/rules.yar) for detection rules covering:
- Stage 1 loader constants (XOR key suffix, known-plaintext bytes)
- Stage 2 hardcoded strings (C2 IP, contract address, ChaCha20 key)

---

## Remediation / Cleanup

If this malware has been executed on a machine:

1. **Isolate immediately** — disconnect from network
2. **Kill processes**: `taskkill /F /IM pythonw.exe`
3. **Remove installation directory**: `%APPDATA%\Tourmaline\` or `%COMMONAPPDATA%\Tourmaline\`
4. **Remove persistence**:
   - Task Scheduler: delete `TourmalineUpdate`
   - Check `HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run` for `Tourmaline` or `SystemService`
5. **Block at firewall**: `158.94.211.185:53/UDP`; block all unexpected outbound UDP/53
6. **Block Ethereum RPC** at proxy: `ethereum-sepolia-rpc.publicnode.com`
7. **Reimage** — due to arbitrary Python exec capability, full reimaging is strongly recommended

---

## Reproducing the Analysis

### Prerequisites
```bash
pip install pyOpenSSL cryptography
```

### Decrypt Stage 2 Payload
```bash
# From the repo root:
python3 src/decrypt_payload.py samples/QGBdu.dxf decrypted_stage2.py
```

### Extract the Malware Sample
```bash
7z x -pinfected samples/Tourmaline_sample.zip
```

---

## Disclosure

| Field | Value |
|---|---|
| **Discovery date** | September 2026 |
| **Researcher** | Vihaan Pundir (v-pun215) |
| **Distribution vector** | ClickFix fake Cloudflare CAPTCHA |
| **Classification** | Backdoor / DNS Tunnel C2 / Blockchain Dead-Drop |
| **Platform** | Windows (64-bit) |

---

## License

See [LICENSE](LICENSE). This repository is for **educational and defensive research purposes only**.

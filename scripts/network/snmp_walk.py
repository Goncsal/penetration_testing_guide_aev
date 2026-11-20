#!/usr/bin/env python3
"""Pure-Python SNMPv1/v2c walker (GETNEXT) — no net-snmp / pysnmp needed.

    python snmp_walk.py snmp1.chal.deti:8024                 # walk from 1.3.6.1
    python snmp_walk.py 127.0.0.1:8024 -c public --oid 1.3.6.1.4.1
    python snmp_walk.py host -c private -v 1 --get 1.3.6.1.2.1.1.1.0
Prints OID = value and highlights flag{...}.
"""
import argparse
import re
import socket

FLAG = re.compile(r"flag\{[^}]+\}")


# ---- minimal BER ----
def enc_len(n):
    if n < 0x80:
        return bytes([n])
    b = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return bytes([0x80 | len(b)]) + b


def tlv(tag, val):
    return bytes([tag]) + enc_len(len(val)) + val


def enc_int(i):
    b = i.to_bytes(max(1, (i.bit_length() + 8) // 8), "big", signed=True)
    return tlv(0x02, b)


def enc_oid(oid):
    parts = [int(x) for x in oid.strip(".").split(".")]
    out = bytes([parts[0] * 40 + parts[1]])
    for p in parts[2:]:
        chunk = [p & 0x7F]
        p >>= 7
        while p:
            chunk.append(0x80 | (p & 0x7F))
            p >>= 7
        out += bytes(reversed(chunk))
    return tlv(0x06, out)


def dec_tlv(buf, i):
    tag = buf[i]
    ln = buf[i + 1]
    i += 2
    if ln & 0x80:
        n = ln & 0x7F
        ln = int.from_bytes(buf[i:i + n], "big")
        i += n
    return tag, buf[i:i + ln], i + ln


def dec_oid(b):
    parts = [b[0] // 40, b[0] % 40]
    v = 0
    for c in b[1:]:
        v = (v << 7) | (c & 0x7F)
        if not c & 0x80:
            parts.append(v)
            v = 0
    return ".".join(map(str, parts))


def build(community, version, pdu_tag, reqid, oid):
    varbind = tlv(0x30, enc_oid(oid) + b"\x05\x00")
    pdu = tlv(pdu_tag, enc_int(reqid) + enc_int(0) + enc_int(0) + tlv(0x30, varbind))
    return tlv(0x30, enc_int(version) + tlv(0x04, community.encode()) + pdu)


def parse(resp):
    _, msg, _ = dec_tlv(resp, 0)
    _, _, i = dec_tlv(msg, 0)          # version
    _, _, i = dec_tlv(msg, i)          # community
    _, pdu, _ = dec_tlv(msg, i)
    _, _, j = dec_tlv(pdu, 0)          # reqid
    _, err, j = dec_tlv(pdu, j)        # error-status
    _, _, j = dec_tlv(pdu, j)          # error-index
    _, vbl, _ = dec_tlv(pdu, j)
    _, vb, _ = dec_tlv(vbl, 0)
    _, oidb, k = dec_tlv(vb, 0)
    vtag, val, _ = dec_tlv(vb, k)
    return int.from_bytes(err, "big"), dec_oid(oidb), vtag, val


def fmt(tag, val):
    if tag == 0x04:
        try:
            return val.decode()
        except UnicodeDecodeError:
            return val.hex()
    if tag in (0x02, 0x41, 0x42, 0x43, 0x46):
        return str(int.from_bytes(val, "big"))
    if tag == 0x06:
        return dec_oid(val)
    if tag == 0x40:
        return ".".join(map(str, val))
    if tag in (0x80, 0x81, 0x82):
        return None
    return val.hex()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", help="host[:port] (default port 161)")
    ap.add_argument("-c", "--community", default="public")
    ap.add_argument("-v", "--version", choices=["1", "2c"], default="2c")
    ap.add_argument("--oid", default="1.3.6.1")
    ap.add_argument("--get", help="single GET of this OID")
    ap.add_argument("--max", type=int, default=5000)
    a = ap.parse_args()
    host, _, port = a.target.partition(":")
    addr = (host, int(port or 161))
    ver = 0 if a.version == "1" else 1
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(3)

    def ask(tag, oid, rid):
        for _ in range(3):
            s.sendto(build(a.community, ver, tag, rid, oid), addr)
            try:
                data, _ = s.recvfrom(65535)
                return parse(data)
            except socket.timeout:
                continue
        raise SystemExit("timeout — wrong community/port/version?")

    if a.get:
        err, oid, tag, val = ask(0xA0, a.get, 1)
        print(f"{oid} = {fmt(tag, val)}")
        return
    cur, root = a.oid, a.oid.strip(".") + "."
    for rid in range(1, a.max):
        err, oid, tag, val = ask(0xA1, cur, rid)
        v = fmt(tag, val)
        if err or v is None or not (oid + ".").startswith(root) or oid == cur:
            break
        print(f"{oid} = {v}")
        for f in FLAG.findall(v):
            print(f"   [FLAG] {f}")
        cur = oid


if __name__ == "__main__":
    main()

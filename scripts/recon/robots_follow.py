#!/usr/bin/env python3
"""Fetch robots.txt (and sitemap.xml) and request every listed path.

    python robots_follow.py http://leak8.chal.deti:8017
"""
import argparse
import re

import requests

FLAG = re.compile(r"flag\{[^}]+\}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("url")
    ap.add_argument("-c", "--cookie")
    a = ap.parse_args()
    base = a.url.rstrip("/")
    hdrs = {"Cookie": a.cookie} if a.cookie else {}
    paths = []
    r = requests.get(base + "/robots.txt", headers=hdrs, timeout=10)
    print(f"[robots.txt {r.status_code}]\n{r.text.strip()}\n")
    for line in r.text.splitlines():
        m = re.match(r"\s*(?:dis)?allow\s*:\s*(\S+)", line, re.I)
        if m and m.group(1) != "/":
            paths.append(m.group(1).replace("*", "").replace("$", ""))
        m = re.match(r"\s*sitemap\s*:\s*(\S+)", line, re.I)
        if m:
            paths.append(m.group(1))
    sm = requests.get(base + "/sitemap.xml", headers=hdrs, timeout=10)
    if sm.status_code == 200:
        paths += re.findall(r"<loc>(.*?)</loc>", sm.text)
    for p in dict.fromkeys(paths):
        url = p if p.startswith("http") else base + "/" + p.lstrip("/")
        try:
            rr = requests.get(url, headers=hdrs, timeout=10)
        except requests.RequestException as e:
            print(f"ERR {url} {e}")
            continue
        listing = " [LISTING]" if re.search(r"index of|<a href", rr.text, re.I) else ""
        print(f"{rr.status_code} {len(rr.content):7d} {url}{listing}")
        for f in FLAG.findall(rr.text):
            print(f"   [FLAG] {f}")


if __name__ == "__main__":
    main()

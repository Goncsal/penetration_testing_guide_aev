#!/usr/bin/env python3
"""First-look probe of a web target.

Prints headers/cookies (stack fingerprint), HTML comments, links, forms,
then requests a list of well-known leak paths and reports anything that is
not a 404 (status, size, title) plus any flag{...} found.

    python quick_probe.py http://leak1.chal.deti:8010
    python quick_probe.py $T -c 'session=abc' --paths ../../wordlists/web/aev-paths.txt
"""
import argparse
import os
import re
import sys

import requests

FLAG = re.compile(r"flag\{[^}]+\}")
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LIST = os.path.join(HERE, "..", "..", "wordlists", "web", "aev-paths.txt")
FALLBACK = ["robots.txt", "sitemap.xml", ".git/HEAD", ".git/logs/HEAD", ".env", "backup/",
            "admin", "debug", "debug/env", "crash", "error", "public/", "static/", "export/",
            "api/", "diagnostics", "status", "phpinfo.php", "server-status", "console", "oracle"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("-c", "--cookie", help="Cookie header value")
    ap.add_argument("--paths", default=DEFAULT_LIST, help="wordlist of paths to probe")
    a = ap.parse_args()
    base = a.url.rstrip("/")
    s = requests.Session()
    if a.cookie:
        s.headers["Cookie"] = a.cookie

    r = s.get(base + "/", timeout=10)
    print(f"[+] GET / -> {r.status_code} ({len(r.content)} bytes)")
    for k, v in r.headers.items():
        if k.lower() in ("server", "x-powered-by", "set-cookie", "www-authenticate", "x-generator",
                         "link", "content-security-policy", "access-control-allow-origin", "x-aspnet-version"):
            print(f"    {k}: {v}")
    body = r.text
    for c in re.findall(r"<!--(.*?)-->", body, re.S):
        print(f"[comment] {c.strip()[:200]}")
    for l in sorted(set(re.findall(r'(?:href|src|action)=["\']([^"\'#]+)', body))):
        print(f"[link] {l}")
    for f in re.findall(r"<form[^>]*>.*?</form>", body, re.S | re.I):
        act = re.search(r'action=["\']([^"\']*)', f)
        meth = re.search(r'method=["\']([^"\']*)', f, re.I)
        names = re.findall(r'name=["\']([^"\']+)', f)
        hidden = re.findall(r'type=["\']hidden["\'][^>]*', f, re.I)
        print(f"[form] {meth.group(1) if meth else 'GET'} {act.group(1) if act else '(self)'} fields={names}")
        for h in hidden:
            print(f"       hidden: {h}")
    for m in FLAG.findall(body):
        print(f"[FLAG] / -> {m}")

    paths = FALLBACK
    if a.paths and os.path.exists(a.paths):
        paths = [l.strip() for l in open(a.paths, encoding="utf-8") if l.strip() and not l.startswith("#")]
    print(f"[+] probing {len(paths)} paths")
    for p in paths:
        try:
            rr = s.get(f"{base}/{p.lstrip('/')}", timeout=8, allow_redirects=False)
        except requests.RequestException as e:
            print(f"    {p}: error {e}")
            continue
        if rr.status_code == 404:
            continue
        title = re.search(r"<title>(.*?)</title>", rr.text, re.S | re.I)
        loc = rr.headers.get("Location", "")
        print(f"    {rr.status_code} {len(rr.content):7d}  /{p.lstrip('/')}  {title.group(1).strip()[:50] if title else ''} {('-> ' + loc) if loc else ''}")
        for m in FLAG.findall(rr.text):
            print(f"[FLAG] /{p} -> {m}")


if __name__ == "__main__":
    sys.exit(main())

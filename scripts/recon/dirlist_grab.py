#!/usr/bin/env python3
"""Walk a directory listing (Apache/nginx/python http.server style), download
every file (recursively) and grep for flags. Optionally save files.

    python dirlist_grab.py http://leak3.chal.deti:8012/public/
    python dirlist_grab.py http://target/export/ --save out/
"""
import argparse
import os
import re
from urllib.parse import urljoin, urlparse, unquote

import requests

FLAG = re.compile(r"flag\{[^}]+\}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url", help="directory URL (with trailing slash)")
    ap.add_argument("--save", help="directory to store downloaded files")
    ap.add_argument("-c", "--cookie")
    ap.add_argument("--depth", type=int, default=3)
    a = ap.parse_args()
    hdrs = {"Cookie": a.cookie} if a.cookie else {}
    root = a.url if a.url.endswith("/") else a.url + "/"
    seen = set()

    def walk(url, depth):
        if url in seen or depth < 0:
            return
        seen.add(url)
        r = requests.get(url, headers=hdrs, timeout=10)
        for href in re.findall(r'href=["\']([^"\'?#]+)', r.text):
            full = urljoin(url, href)
            if not full.startswith(root) or full == url or href in ("../", "/"):
                continue
            if full.endswith("/"):
                walk(full, depth - 1)
                continue
            if full in seen:
                continue
            seen.add(full)
            fr = requests.get(full, headers=hdrs, timeout=10)
            print(f"{fr.status_code} {len(fr.content):8d} {unquote(urlparse(full).path)}")
            for f in FLAG.findall(fr.content.decode("utf-8", "ignore")):
                print(f"   [FLAG] {f}")
            if a.save:
                rel = unquote(full[len(root):])
                dst = os.path.join(a.save, *rel.split("/"))
                os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
                open(dst, "wb").write(fr.content)

    walk(root, a.depth)


if __name__ == "__main__":
    main()

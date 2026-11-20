#!/usr/bin/env python3
"""Same-origin crawler that reports links, forms (incl. hidden fields),
HTML comments, paths mentioned in text (<code>/x/y</code>), tokens in URLs
and flags.

    python crawl.py http://target
    python crawl.py http://target -c 'session=...' --max 300
"""
import argparse
import re
from collections import deque
from urllib.parse import urljoin, urlparse, urldefrag

import requests

FLAG = re.compile(r"flag\{[^}]+\}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("-c", "--cookie")
    ap.add_argument("--max", type=int, default=200)
    a = ap.parse_args()
    start = a.url if a.url.endswith("/") else a.url + "/"
    origin = urlparse(start).netloc
    s = requests.Session()
    if a.cookie:
        s.headers["Cookie"] = a.cookie
    seen, q = set(), deque([start])
    mentioned, tokens, flags = set(), set(), set()
    while q and len(seen) < a.max:
        url = q.popleft()
        if url in seen:
            continue
        seen.add(url)
        try:
            r = s.get(url, timeout=8)
        except requests.RequestException as e:
            print(f"ERR {url} {e}")
            continue
        ctype = r.headers.get("Content-Type", "")
        print(f"{r.status_code} {len(r.content):7d} {url}")
        text = r.text
        flags.update(FLAG.findall(text))
        if "html" not in ctype and "javascript" not in ctype and "text" not in ctype:
            continue
        for c in re.findall(r"<!--(.*?)-->", text, re.S):
            print(f"    [comment] {c.strip()[:300]}")
        for f in re.findall(r"<form[^>]*>.*?</form>", text, re.S | re.I):
            act = re.search(r'action=["\']([^"\']*)', f)
            meth = re.search(r'method=["\']([^"\']*)', f, re.I)
            inputs = re.findall(r"<(?:input|textarea|select)[^>]*>", f, re.I)
            fields = []
            for i in inputs:
                n = re.search(r'name=["\']([^"\']+)', i)
                v = re.search(r'value=["\']([^"\']*)', i)
                t = re.search(r'type=["\']([^"\']+)', i)
                fields.append(f"{n.group(1) if n else '?'}{'(' + t.group(1) + ')' if t else ''}={v.group(1) if v else ''}")
            print(f"    [form] {(meth.group(1) if meth else 'GET').upper()} {act.group(1) if act else url} {fields}")
        for m in re.findall(r"<code>(/[\w./-]+)</code>", text):
            mentioned.add(m)
        for m in re.findall(r"[?&](?:sid|token|session|key|auth|reset)=[\w.-]+", text):
            tokens.add(m)
        for link in re.findall(r'(?:href|src|action)=["\']([^"\']+)', text):
            nxt, _ = urldefrag(urljoin(url, link))
            if urlparse(nxt).netloc == origin and nxt not in seen and not nxt.startswith("javascript:"):
                q.append(nxt)
    if mentioned:
        print("\n[paths mentioned in text but maybe not linked]")
        for m in sorted(mentioned):
            print("   ", m)
    if tokens:
        print("\n[tokens in URLs]")
        for t in sorted(tokens):
            print("   ", t)
    if flags:
        print("\n[FLAGS]")
        for f in sorted(flags):
            print("   ", f)


if __name__ == "__main__":
    main()

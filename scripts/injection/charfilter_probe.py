#!/usr/bin/env python3
"""Find out which characters/words a filter strips or blocks.

Sends MARK<x>MARK for each candidate and reports: passed (echoed intact),
stripped (MARKMARK echoed), blocked (status differs / error) or unknown.

    python charfilter_probe.py "http://inj2.chal.deti:8041/label" --data "sku=A1&text=FUZZ"
    python charfilter_probe.py "http://t/run?cmd=FUZZ"
"""
import argparse
from urllib.parse import quote

import requests

CANDS = [";", "|", "&", "$", "`", "\n", "\r", ">", "<", "(", ")", "{", "}", "*", "?", "[", "]", "'", '"',
         "\\", "/", " ", "\t", "#", "%", "!", "~", "=", "$(", "${IFS}", "&&", "||", "..", "flag", "cat",
         "etc", "passwd", "sh", "bash", "curl", "wget", "nc", "python", "<script", "onerror", "union", "select"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--data")
    ap.add_argument("-c", "--cookie")
    a = ap.parse_args()
    hdr = {"Cookie": a.cookie} if a.cookie else {}

    def send(v):
        q = quote(v, safe="")
        if a.data:
            return requests.post(a.url, data=a.data.replace("FUZZ", q), timeout=15,
                                 headers={**hdr, "Content-Type": "application/x-www-form-urlencoded"})
        return requests.get(a.url.replace("FUZZ", q), headers=hdr, timeout=15)

    base = send("MARKxMARK")
    print(f"baseline {base.status_code} (echo={'MARKxMARK' in base.text})")
    for c in CANDS:
        r = send(f"MARK{c}MARK")
        if r.status_code != base.status_code:
            res = f"BLOCKED ({r.status_code})"
        elif f"MARK{c}MARK" in r.text:
            res = "passed"
        elif "MARKMARK" in r.text:
            res = "STRIPPED"
        else:
            res = "? (not echoed / transformed)"
        print(f"{c!r:12} {res}")


if __name__ == "__main__":
    main()

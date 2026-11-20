#!/usr/bin/env python3
"""Generate context password candidates from words (company, product, names, years).

    python mutate.py brightleaf vpn 2024 > ctx.txt
"""
import itertools
import sys

words = sys.argv[1:] or ["admin"]
years = [w for w in words if w.isdigit()] or ["2023", "2024", "2025", "2026"]
bases = [w for w in words if not w.isdigit()]
seasons = ["Spring", "Summer", "Autumn", "Fall", "Winter"]
suffixes = ["", "1", "12", "123", "1234", "!", "1!", "123!", "@123", "#1", "01"]
out = set()
for b in bases + seasons + ["Welcome", "Password", "Passw0rd", "Admin", "Qwerty", "Changeme", "Letmein"]:
    for form in {b, b.lower(), b.capitalize(), b.upper()}:
        for s in suffixes:
            out.add(form + s)
        for y in years:
            for s in ["", "!", "@", "#"]:
                out.add(form + y + s)
                out.add(form + y[-2:] + s)
leet = str.maketrans("aeios", "43105")
for w in list(out):
    out.add(w.translate(leet))
for w in sorted(out):
    print(w)

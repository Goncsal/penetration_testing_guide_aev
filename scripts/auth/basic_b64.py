#!/usr/bin/env python3
"""Turn a user:pass combo list into base64 tokens for ffuf Basic-auth fuzzing.

    python basic_b64.py combos.txt > b64.txt
    ffuf -u http://t/admin -H 'Authorization: Basic FUZZ' -w b64.txt -mc 200
"""
import base64
import sys

for line in open(sys.argv[1], encoding="utf-8", errors="ignore"):
    line = line.rstrip("\r\n")
    if line:
        print(base64.b64encode(line.encode()).decode())

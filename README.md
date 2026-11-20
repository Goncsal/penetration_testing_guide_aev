# AEV Pentest Field Guide

A tree of small, linked notes built from the **AEV course decks** (Vulnerabilities, Vulnerability
Assessment, Enumeration & Information Leakage, Command Injection, Authentication Failures, XSS) and
the **57 course CTF challenges** (`auth`, `infoleak`, `inj`, `sqli`, `web`, `network`, `pwn`).

Goal: land on an unknown challenge, follow the links, get the flag — using only this repo.

## How to use it

```
START ─► 00-start/01-first-10-minutes.md      (recon every challenge the same way)
      ─► 00-start/02-what-vuln-is-it.md        (symptom → most-likely vuln class)
      ─► <category>/README.md                  (triage inside the class)
      ─► <technique>.md                        (test → exploit, payloads)
      ─► tools/<tool>.md  or  scripts/<x>.py   (how to run it)
      ─► 00-start/04-where-is-the-flag.md      (flag found? no → keep reading)
```

Every technique note has the same shape: **Signs → Confirm → Exploit → Bypasses → Seen in → Next**.

## Map

| Folder | What's inside |
|---|---|
| [00-start](00-start/) | Methodology, triage table, hint-reading, flag locations, local lab, CVE research, write-ups |
| [01-recon](01-recon/README.md) | Port scan, fingerprinting, content discovery, vhosts, parameters |
| [02-info-leak](02-info-leak/README.md) | Comments, backups, listings, `.git`, debug routes, errors, JS secrets, oracles |
| [03-auth](03-auth/README.md) | Default creds, brute force, enumeration, cookies, sessions, JWT, reset tokens |
| [04-access-control](04-access-control/README.md) | IDOR, hidden params, forced browsing, method tampering |
| [05-injection](05-injection/README.md) | OS cmd injection (+filters, WAF, 2nd order, PATH), SSTI, XXE, SSRF, deserialization, LFI, upload |
| [06-sqli](06-sqli/README.md) | Detection, auth bypass, UNION, error, boolean, time, OOB, INTO OUTFILE, INSERT |
| [07-xss-client-side](07-xss-client-side/README.md) | Reflected / stored / DOM XSS, filter bypass, cookie theft, CSRF, CORS |
| [08-vuln-apps](08-vuln-apps/README.md) | DVWA, bWAPP, Juice Shop, Mutillidae, WordPress (incl. admin → reverse shell) |
| [09-network](09-network/README.md) | SNMP and other non-HTTP services |
| [10-pwn](10-pwn/README.md) | Stack overflow / ret2win and beyond |
| [11-post-exploitation](11-post-exploitation/README.md) | Reverse shells, upgrading shells, finding flags, privesc basics |
| [tools](tools/README.md) | One short page per tool: install, best flags for these challenges |
| [scripts](scripts/README.md) | Reusable Python exploits (generic, take URL/args) |
| [wordlists](wordlists/README.md) | Curated lists (SecLists subsets + course-specific lists) |
| [challenges](challenges/README.md) | The 57 known course challenges → which note solves them |

## Conventions

- `$T` = target base URL, e.g. `export T=http://inj1.chal.deti:8040` (lab) or `http://127.0.0.1:8040` (local).
- Flags look like `flag{...}`. Always grep: `curl -s $T | grep -o 'flag{[^}]*}'`.
- Scripts: `python scripts/<area>/<name>.py -h` for usage. Only dependency for most: `pip install requests`.
- Only test systems you're authorised to (the course lab / your local containers).

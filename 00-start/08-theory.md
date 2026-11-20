# Theory cheat sheet (decks 1–2)

Short reference for the non-hands-on parts of the course.

## Vulnerabilities (deck 1)
- **Vulnerability**: weakness that lets an attacker violate a reasonable security policy.
- Taxonomies: **OWASP Top 10** (web), **7 Pernicious Kingdoms** (input validation, API abuse,
  security features, time & state, errors, code quality, encapsulation, environment), **CWE**.
- **CVE**: ID assigned by a CNA; **NVD** enriches (but has a backlog — many CVEs lack CVSS/CPE now).
- **CVSS v4.0**: Base (exploitability + impact) + Threat (PoC/exploited?) + Environmental
  (v3.1: Base + Temporal + Environmental). Also use **KEV** (known exploited) and **EPSS** (probability).
- **Disclosure**: none (0-day), full, coordinated/responsible; `security.txt` (RFC 9116), CSIRT
  RFC 2350, national CERT, bug bounties vs. brokers.

## Vulnerability assessment (deck 2)
- Asset, vulnerability, threat, control; **Risk = f(threat, vulnerability, impact)**.
- Assessment ≠ audit (compliance) ≠ pentest (prove entry & impact).
- Types: active/passive, external/internal, host/network/application/wireless — better described on
  4 axes: **method, vantage point, target, knowledge** (black/grey/white box).
- **Scope + written authorisation + Rules of Engagement** before any probe.
- Lifecycle: baseline → assessment → risk assessment → remediation → verification → monitoring.
- Quality: false positives vs **false negatives** (invisible), coverage.
- **SCAP**: CPE (platforms), CVE, CVSS, CCE (configs), XCCDF (checklists/profiles), OVAL (checks),
  OCIL (questionnaires). Tools: OpenSCAP, Greenbone/OpenVAS, Nessus.

## Enumeration & information leakage (deck 2b)
- Leaks: broadcast protocols, **banners**, **errors** (CWE-204 account leaks, CWE-209 stack traces),
  web support files (comments, `robots.txt`, `phpinfo()`), **cookie names** (stack disclosure),
  **ports** (open/closed/filtered), **OS fingerprinting** (nmap `-O`, TCP T2–T7 probes).
- Mitigations: generic errors with error codes, strip version banners, firewall detection of scans,
  minimal open ports.
- Hands-on: [01-recon](../01-recon/README.md), [02-info-leak](../02-info-leak/README.md).

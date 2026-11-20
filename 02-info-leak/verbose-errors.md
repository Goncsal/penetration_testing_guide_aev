# Verbose errors & stack traces (CWE-209)

**Signs**: hint "make it stumble", "spill its insides"; 500 pages with code; DB errors shown.

## Make it crash
```bash
curl -s "$T/crash"; curl -s "$T/error"; curl -s "$T/500"
curl -s "$T/item?id='"            # quote → SQL error (also an SQLi signal!)
curl -s "$T/item?id[]=1"          # array where string expected (PHP/Express)
curl -s "$T/item?id=abc"          # string where int expected
curl -s "$T/%"  "$T/%00"          # bad encoding
curl -s -X POST $T/api -H 'Content-Type: application/json' -d '{bad json'
curl -s -X PUT $T/                # unexpected method
```
Fuzz all params with weird values: `wordlists/fuzz/special-chars.txt`.

## What to read in the trace
- **Secrets inline** (the flag, keys, connection strings) — `leak10`.
- File paths (`/app/app.py`) → backup hunting, LFI targets.
- Framework + version → [06-cve-research](../00-start/06-cve-research.md).
- **SQL query text** → shape your SQLi ([06-sqli](../06-sqli/README.md)).
- Werkzeug debugger traceback (interactive console if not PIN-locked).

## Response discrepancy (CWE-204)
Different error **text, status, length or timing** for different inputs = an oracle:
- login: "no such user" vs "wrong password" → [user-enumeration](../03-auth/user-enumeration.md)
- search count / row present / slower → [blind SQLi](../06-sqli/boolean-blind.md)
- prefix check → [oracles](oracles.md)

Seen in: `leak10` (`/crash` returns a traceback containing the flag), `sqli2` (DB error echoed).

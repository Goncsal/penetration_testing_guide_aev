# Where is the flag?

Flag format: `flag{...}`. Per-student, injected at deploy time; some **roll** (change after each
correct solve) — so always extract it live, never reuse.

## Where course challenges keep it

| Location | Typical for | How you reach it |
|---|---|---|
| Rendered in a page only a privileged user sees (`/admin`, `/dashboard`, `/manager`, `/record`) | auth | become that user → [03-auth](../03-auth/README.md) |
| A response field you don't normally get (`?verbose=true`, hidden JSON key) | infoleak / IDOR | [idor](../04-access-control/idor.md) |
| HTML comment, JS file, backup file, `.git` log, debug env dump, stack trace | infoleak | [02-info-leak](../02-info-leak/README.md) |
| **File `/flag/flag`** (live mount; app dir may hold a **decoy** `flag{...}`) | inj | command exec / file read → `cat /flag/flag` |
| `/etc/lab_flag`, `/flag.txt`, `/root/flag`, `$FLAG` env var | RCE challenges | [find-the-flag](../11-post-exploitation/find-the-flag.md) |
| DB table not shown by the UI (`vault`, `secret`, `flags`, `users.notice`) | sqli | [06-sqli](../06-sqli/README.md) |
| `/flag` endpoint that requires a cookie set by page JS (`grant()`) | xss | [07-xss](../07-xss-client-side/README.md) |
| SNMP private OID tree (`1.3.6.1.4.1.*`) | network | [snmp](../09-network/snmp.md) |
| Printed by a `win()` function in the binary | pwn | [ret2win](../10-pwn/ret2win.md) |
| Per-exercise in DVWA/bWAPP/Juice Shop/Mutillidae | web | [08-vuln-apps](../08-vuln-apps/README.md) |

## Grep everything

```bash
curl -s $T/whatever | grep -o 'flag{[^}]*}'
python scripts/lib/flaggrep.py file_or_dir_or_url     # recursive, also decodes base64/hex/url
```

The flag may come back **HTML-escaped** (`&lt;`) or **URL-encoded** — unescape before grepping
(`python -c "import html,sys;print(html.unescape(sys.stdin.read()))"`).

## Got RCE but no flag?

```bash
cat /flag/flag /flag* /etc/lab_flag /root/flag* 2>/dev/null; env | grep -i flag
find / -iname '*flag*' -not -path '/proc/*' -not -path '/sys/*' 2>/dev/null
grep -rIs 'flag{' /app /srv /var/www /opt /home /tmp 2>/dev/null | head
```
If a path filter blocks the word `flag`: [cmdi-filter-bypass](../05-injection/cmdi-filter-bypass.md#word-filter-eg-flag-blocked).

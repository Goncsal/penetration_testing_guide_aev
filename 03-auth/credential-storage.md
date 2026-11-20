# Leaked credential stores (CWE-256, CWE-257, CWE-522, CWE-916)

You found a dump (`.sql`, `.bak`, `users.json`, `/etc/shadow`, `.env`). Identify what the
"password" column really is:

| Looks like | It is | Do |
|---|---|---|
| readable text | cleartext | log in |
| ends in `=`/`==`, `[A-Za-z0-9+/]` | **base64** ("encrypted"!) | `echo '...' \| base64 -d` |
| `[0-9a-f]{32}` | MD5 (or NTLM) | crack: hashcat `-m 0` / crackstation |
| `[0-9a-f]{40}` | SHA-1 | `-m 100` |
| `[0-9a-f]{64}` | SHA-256 | `-m 1400` |
| `$2a$`/`$2b$`/`$2y$` | bcrypt | `-m 3200` (slow — small wordlist) |
| `$argon2id$` | Argon2 | very slow — guess only top-1000 |
| `$1$` / `$5$` / `$6$` | md5crypt / sha256crypt / sha512crypt | `-m 500` / `7400` / `1800` |
| `pbkdf2_sha256$...` | Django | `-m 10000` |
| `$P$` / `$H$` | WordPress phpass | `-m 400` |
| hex + separate salt column | salted hash | `-m 10`/`20`… (`hash:salt`) |

```bash
hashid '<hash>'                                         # identify
hashcat -m 0 hashes.txt wordlists/passwords/10k-most-common.txt
john --wordlist=wordlists/passwords/10k-most-common.txt hashes.txt
```
→ [tools/hashcat-john.md](../tools/hashcat-john.md). Also try decoding as hex / ROT13 / XOR with
CyberChef "Magic".

Then log in as that user (often `admin`) and read the privileged page.

Seen in: `auth12` (`/robots.txt` → `/export/` listing → `cornerstone_staging.sql.bak` →
`password_encrypted` = base64 → admin login → `/dashboard`).

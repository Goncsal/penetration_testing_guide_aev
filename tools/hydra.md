# hydra

Online brute forcer for many protocols.

```bash
# HTTP Basic auth
hydra -L users.txt -P pass.txt -s 8060 host http-get /admin
hydra -C wordlists/passwords/default-creds-combo.txt -s 8060 host http-get /admin   # user:pass combos
# HTML form (POST) — "path:body:F=failure string"  (or S=success string)
hydra -l vpnuser -P wordlists/passwords/top-1000.txt -s 8072 host \
  http-post-form '/login:username=^USER^&password=^PASS^:F=Invalid'
# with cookie / header
hydra ... http-post-form '/login:u=^USER^&p=^PASS^:F=Invalid:H=Cookie: security=low'
# other services
hydra -l root -P pass.txt ssh://host ; hydra -L u.txt -P p.txt ftp://host
```
| Option | Meaning |
|---|---|
| `-l`/`-L` | one user / user list |
| `-p`/`-P` | one password / list |
| `-C` | `user:pass` combo file |
| `-s` | port |
| `-t 4` | parallel tasks (lower for fragile apps) |
| `-f` | stop at first hit |
| `-V` | show every attempt |
| `https-post-form` | TLS |

Hydra can't handle per-request CSRF tokens → use `scripts/auth/login_brute.py --csrf-field`.

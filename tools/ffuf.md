# ffuf — Fuzz Faster U Fool

Replaces the word `FUZZ` anywhere in the request (URL, header, body, cookie) with each wordlist
entry and filters the responses. Install: `apt install ffuf` / `go install github.com/ffuf/ffuf/v2@latest`.

## The 6 flags that matter
| Flag | Meaning |
|---|---|
| `-u URL` | target; put `FUZZ` where words go |
| `-w list[:KEYWORD]` | wordlist (several with custom keywords: `-w users.txt:U -w pass.txt:P`) |
| `-mc` / `-fc` | match / filter status codes (`-mc all -fc 404`) |
| `-fs` / `-fw` / `-fl` | filter by size / words / lines (remove the "nothing found" page) |
| `-fr` / `-mr` | filter / match regex in the body (`-fr 'Invalid password'`, `-mr 'flag\{'`) |
| `-ac` | auto-calibrate: learns the "not found" response and filters it |

Others: `-X POST`, `-d 'a=FUZZ'`, `-H 'Cookie: x=y'`, `-b 'cookie'`, `-e .bak,.php` (extensions),
`-recursion -recursion-depth 2`, `-t 40` (threads; lower to 5–10 for fragile lab apps),
`-rate 50`, `-p 0.1` (delay), `-o out.json`, `-x http://127.0.0.1:8080` (through Burp),
`-mode clusterbomb|pitchfork` (multi-wordlist), `-c` colour, `-v` full URL.

## Recipes for this course
```bash
# paths: course list first, then generic
ffuf -u $T/FUZZ -w wordlists/web/aev-paths.txt -mc all -fc 404
ffuf -u $T/FUZZ -w wordlists/web/common.txt -mc all -fc 404 -ac
# files + extensions
ffuf -u $T/FUZZ -w wordlists/web/common.txt -e .bak,.old,.txt,.php,.py,.zip,.sql -mc 200 -ac
# backup of a known file
ffuf -u $T/static/config.pyFUZZ -w wordlists/web/backup-suffixes.txt -mc 200
# GET parameter names (filter baseline size)
ffuf -u "$T/api/users/1?FUZZ=true" -w wordlists/web/burp-parameter-names.txt -fs 123
# IDOR ids
seq 1 500 > /tmp/ids; ffuf -u $T/note/FUZZ -w /tmp/ids -b 'session=...' -mc 200
# login brute force (filter the failure message)
ffuf -u $T/login -X POST -H 'Content-Type: application/x-www-form-urlencoded' \
     -d 'username=admin&password=FUZZ' -w wordlists/passwords/top-1000.txt -fr 'Invalid'
# user enumeration
ffuf -u $T/login -X POST -H 'Content-Type: application/x-www-form-urlencoded' \
     -d 'user=FUZZ&password=x' -w wordlists/usernames/names.txt -fr 'No such user'
# user:pass both (clusterbomb)
ffuf -u $T/login -X POST -d 'u=U&p=P' -w users.txt:U -w pass.txt:P -fr 'Invalid' -H 'Content-Type: application/x-www-form-urlencoded'
# vhosts
ffuf -u $T/ -H 'Host: FUZZ.target.tld' -w wordlists/web/subdomains-top5000.txt -fs <default_size>
# header fuzz (IP-trust headers)
ffuf -u $T/admin -H 'FUZZ: 127.0.0.1' -w wordlists/web/ip-headers.txt -mc 200
# injection payload lists
ffuf -u "$T/view?file=FUZZ" -w wordlists/fuzz/lfi-jhaddix.txt -mr 'root:x:0:0'
ffuf -u "$T/?q=FUZZ" -w wordlists/xss/xss-payloads.txt -mr 'onerror'
```

## Tips
- Always check one bad request first (`curl -s -o /dev/null -w '%{http_code} %{size_download}'`)
  to know what to filter.
- Raw request from Burp: save to `req.txt` with `FUZZ` inside, `ffuf -request req.txt -request-proto http -w ...`.
- Many 200s of the same size = soft-404 → use `-fs` or `-ac`.

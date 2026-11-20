# Wordlists

Small/medium lists live in the repo (≈3 MB). Big ones (rockyou, directory-list-2.3-medium…):
`bash wordlists/fetch_big.sh` → `wordlists/big/` (git-ignored). Sources: SecLists
(danielmiessler/SecLists, MIT), wallarm/jwt-secrets; files marked *custom* were written for this
course.

## web/ — content discovery
| File | Lines | Use first for |
|---|---|---|
| `aev-paths.txt` *custom* | ~180 | **start here**: every route seen in the course + classic leak paths |
| `common.txt` | ~4.7k | general dirs/files |
| `quickhits.txt` | ~2.5k | known sensitive files (configs, admin panels) |
| `raft-small-files.txt` | ~11k | filenames with extensions |
| `raft-medium-directories.txt` | ~30k | deeper directory fuzz |
| `backup-suffixes.txt` *custom* | | `ffuf -u $T/config.pyFUZZ` |
| `backup-files.txt` *custom* | | whole-site/db backups, `*.bak` configs |
| `burp-parameter-names.txt` | ~6k | hidden GET/POST params |
| `api-endpoints.txt` | | `/api/FUZZ` |
| `wordpress.txt` | | WordPress paths |
| `cgi-scripts.txt` *custom* | | `/cgi-bin/FUZZ` (Shellshock) |
| `subdomains-top5000.txt` | 5k | vhost fuzzing |
| `ip-headers.txt` *custom* | | IP-trust header names (`FUZZ: 127.0.0.1`) |
| `default-web-roots-linux.txt` | | where to write a webshell |

## passwords/ & usernames/
| File | Use |
|---|---|
| `passwords/top-100.txt`, `top-1000.txt` (xato) | first online guesses (`qwerty` is in top-100) |
| `passwords/top-passwords-shortlist.txt` | 20 most common |
| `passwords/10k-most-common.txt` | longer online / quick offline |
| `passwords/default-creds-combo.txt` *custom+SecLists* | `user:pass` defaults (routers, Tomcat, SSH, FTP, bWAPP, DVWA…) |
| `passwords/default-passwords.csv` | vendor default credential DB (grep the product) |
| `passwords/{tomcat,ssh,ftp}-default-combos.txt` | per-service combos |
| `usernames/top-usernames-shortlist.txt` | admin, root, test… |
| `usernames/names.txt` | first names (pair with `scripts/auth/username_gen.py`) |
| `big/rockyou.txt` (fetch) | offline cracking / last-resort online |

## secrets/
| File | Use |
|---|---|
| `jwt-secrets.txt` (wallarm, ~100k) | JWT HMAC cracking (`jwt_tool_lite.py crack -w`, hashcat 16500) |
| `flask-secret-keys.txt` *custom* | `flask-unsign --unsign` quick list (then try jwt-secrets.txt) |

## fuzz/, sqli/, xss/, network/
| File | Use |
|---|---|
| `fuzz/cmdi-quick.txt` *custom* | command injection probes (separators, substitution, newline, glob) |
| `fuzz/command-injection-commix.txt` | huge cmdi list (commix) |
| `fuzz/ssti-probes.txt` *custom*, `ssti-identification.txt`, `ssti-expression.txt` | template injection |
| `fuzz/lfi-jhaddix.txt` | path traversal / LFI |
| `fuzz/special-chars.txt` | break parsers / provoke errors |
| `fuzz/http-methods.txt` | verb tampering |
| `fuzz/common-ports.txt` *custom* | SSRF internal port scan |
| `sqli/auth-bypass.txt` *custom*, `seclists-auth-bypass.txt` | login bypass |
| `sqli/quick-sqli.txt`, `generic-sqli.txt`, `generic-blind-sqli.txt`, `polyglots.txt` | detection |
| `xss/xss-payloads.txt` *custom+BruteLogic+polyglots* | quick XSS fuzz |
| `xss/xss-jhaddix.txt`, `xss-brutelogic.txt`, `xss-polyglots.txt` | more XSS |
| `network/snmp-communities.txt` | `onesixtyone -c` |

How to use them with ffuf: [tools/ffuf.md](../tools/ffuf.md).

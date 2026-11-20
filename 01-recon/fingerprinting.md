# Fingerprinting (banners, headers, cookies)

Knowing the stack tells you which payload dialect to use (Jinja vs EJS SSTI, SQLite vs MySQL, PHP
vs Python) and which CVEs apply.

## HTTP

```bash
curl -sI $T                          # headers only
curl -s -D - -o /dev/null $T         # headers of a GET
whatweb -a 3 $T                      # tools/whatweb-nikto.md
```

| Header / cookie | Means |
|---|---|
| `Server: Werkzeug/x Python/3.x` | Flask dev server → Jinja2 SSTI, pickle, `/console` debugger |
| `Server: gunicorn` | Python (Flask/Django) |
| `X-Powered-By: Express` | Node.js → EJS/Pug/Handlebars SSTI, prototype pollution |
| `X-Powered-By: PHP/x`, `PHPSESSID` | PHP → LFI, `include`, type juggling, webshell upload |
| `JSESSIONID` | Java (Tomcat/Spring) → XXE, deserialization (`rO0AB`), EL injection |
| `ASP.NET_SessionId`, `.AspNetCore.*`, `X-AspNet-Version` | .NET |
| `session=eyJ...` (Flask) | Flask signed cookie — decode with `flask-unsign --decode` |
| `connect.sid=s%3A...` | Express-session |
| `Link: <.../wp-json/>` , `wordpress_*` cookies | WordPress → [wordpress](../08-vuln-apps/wordpress.md) |
| `Server: Apache/2.4.x (Debian)` | OS distro + version → CVE lookup |

## Error pages fingerprint too
Request a missing page and a malformed one (`/%`, `/'`, `?id[]=1`): the error page style names the
framework → [verbose-errors](../02-info-leak/verbose-errors.md).

## Other services
```bash
nc -nv <host> 21          # FTP/SMTP/SSH speak first: read the banner
ssh -v user@host          # "remote software version OpenSSH_7.2"
nmap -sV -p <port> <host>
```
Then: [00-start/06-cve-research.md](../00-start/06-cve-research.md)

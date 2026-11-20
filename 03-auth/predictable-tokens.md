# Predictable session / reset tokens (CWE-330, CWE-331)

**Signs**: token is a hash-looking hex string (32 = MD5, 40 = SHA-1, 64 = SHA-256) or short number;
two logins in the same second give the same token; a "refresh"/"rotate"/"re-auth" button makes a
privileged account log in *now*. Hint "minted from a clock", "a second's width".

## 1. Guess the recipe
Log in a few times and try candidate inputs offline:
```bash
python scripts/auth/token_recipe.py <observed_token> --user agent --ts-window 30
```
It tries md5/sha1/sha256 of combos like `user`, `user:ts`, `ts`, `user+ts`, `reset:user`,
`user:ts_ms`… around the current time and reports which reproduces your token.

Common bad recipes: `hash(username)`, `hash(username + timestamp)`, `hash("reset:" + username)[:20]`,
`uuid1()` (time-based), `random.seed(time)`, incrementing ints, `base64(user:time)`.

## 2. Predict the victim's token
```bash
# trigger the admin login (bot/refresh endpoint) and record your clock around it
python scripts/auth/ts_token_brute.py $T --trigger /bot/refresh-oncall \
      --check /ticket/admin --cookie-name token --fmt 'sha1:admin:{ts}' --window 5
```
`--fmt` = `algo:template` with `{ts}` (unix seconds), `{ms}` (milliseconds) or `{user}`.
Clock skew? widen `--window`. Token as header/param? `--header` / `--param`.

## 3. Randomness check
Collect 50+ tokens (Burp Sequencer) — low entropy, sequential bytes or repeated prefixes ⇒ brute
the small space.

Seen in: `auth9` (`sha1("admin:<unix_ts>")` minted by `/bot/refresh-oncall`, checked on
`/ticket/admin` via `token` cookie), `auth11` (reset token `sha256("reset:"+user)[:20]` →
[password-reset](password-reset.md)).

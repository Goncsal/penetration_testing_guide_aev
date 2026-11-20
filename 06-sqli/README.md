# 06 — SQL injection (CWE-89)

## Decision tree

```
Is it injectable?  ─────────────────────────────►  detection.md
        │
        ▼
Login form?  ── yes ──►  auth-bypass.md  (admin' -- )
        │
        ▼  What feedback do you get?
  query results rendered on page ......................► union-based.md
  DB error text shown ..................................► error-based.md
  only a count / a row appears or not / true-false .....► boolean-blind.md
  nothing at all, same page every time .................► time-blind.md
  the app *fetches* / *emails* / *uses* a returned value ► out-of-band.md
  app writes query results to a file / exports a table .► file-read-write.md
  input goes into INSERT/UPDATE (signup, guestbook) ....► insert-update.md
```

Know the DBMS → syntax: [dbms-cheatsheet.md](dbms-cheatsheet.md). Automate when allowed:
[tools/sqlmap.md](../tools/sqlmap.md).

## Where the flag usually is
A table the UI never shows (`vault`, `secret(s)`, `flag(s)`, `config`), a column of a row you can't
normally see (admin's `notice`), or a file on disk. List tables first
([dbms-cheatsheet](dbms-cheatsheet.md#enumerate-schema)).

Course map: sqli1 login bypass (SQLite) · sqli2 error-based `updatexml` (MariaDB) · sqli3 UNION 4
cols (SQLite) · sqli4 boolean/count + binary search (SQLite) · sqli5 boolean/marker row (SQLite) ·
sqli6 time-based in INSERT (MariaDB) · sqli7 UNION → app fetches URL (OOB, SQLite) · sqli8 table
name → `INTO OUTFILE` (MariaDB).

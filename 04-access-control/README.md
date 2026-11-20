# 04 — Broken access control

Authentication works, **authorization** doesn't: the server knows who you are but doesn't check
whether *you* may access *that* object/function.

| Symptom | Note |
|---|---|
| Object ids in URLs/APIs (`/note/3`, `/api/users/12`, `?invoice=1001`) | [idor](idor.md) |
| Extra fields in responses with a flag param (`?verbose=true`, `?fields=*`) | [idor](idor.md#hidden-fields--verbose-switches) |
| Admin pages you weren't linked to; 403 on a page | [forced-browsing](forced-browsing.md) |
| JSON/forms where you could add `role`, `isAdmin`, `owner` | [mass-assignment](mass-assignment.md) |
| Role in cookie / hidden field | [client-side-trust](../03-auth/client-side-trust.md) |

Course map: `notes1` (note 3 owned by admin), `leak5` (admin profile id + `verbose=true`),
DVWA/bWAPP/Juice Shop "IDOR / broken access control" exercises.

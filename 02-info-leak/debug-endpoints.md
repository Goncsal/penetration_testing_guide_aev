# Debug / diagnostic routes

**Signs**: hint "back room", "the machine confesses"; dev frameworks; nothing linked.

Fuzz with the course list first (it contains these):
```bash
ffuf -u $T/FUZZ -w wordlists/web/aev-paths.txt -mc all -fc 404
```

| Path | What it gives |
|---|---|
| `/debug`, `/debug/env`, `/env`, `/environment`, `/_debug`, `/__debug__` | environment vars (flags, secrets) |
| `/diagnostics`, `/status`, `/health`, `/metrics`, `/info`, `/stats` | internals, **session ids**, logs |
| `/console` (Werkzeug) | Python console (PIN-protected; PIN leaks via `/proc` + LFI) |
| `/actuator/env`, `/actuator/heapdump`, `/actuator/mappings` (Spring) | env, memory dump, all routes |
| `/phpinfo.php`, `/info.php`, `/test.php` | full PHP config, env vars, paths |
| `/server-status`, `/server-info` (Apache) | live requests (URLs with tokens!) |
| `/.env`, `/config.json`, `/settings.json` | secrets |
| `/swagger`, `/api-docs`, `/graphql` (introspection) | every API route |
| `/admin`, `/manage`, `/internal`, `/staff`, `/ops` | admin panels → test auth |

Also try debug **parameters** on normal pages: `?debug=1`, `?debug=true`, `?test=1`, `?verbose=1`,
`?_debug=1` and headers `X-Debug: 1` → [parameter-discovery](../01-recon/parameter-discovery.md).

Seen in: `leak2` (`/debug/env` dumps env with flag), `auth14` (`/diagnostics` lists stale session
ids → [session-hijack](../03-auth/session-hijack.md)).

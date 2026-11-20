# Out-of-band listeners (catch callbacks)

Needed for: blind cmdi exfil, SQLi OOB (`sqli7`), SSRF/XXE confirmation, XSS cookie theft.

## Your own HTTP catcher
```bash
python scripts/xss/catch_server.py --port 8000          # logs every request (path, query, body), CORS-friendly
sudo python scripts/xss/catch_server.py --port 443      # lab: egress only allows 80/443 → bind 80/443 (root)
python -m http.server 80                                # simplest (shows path+query in the log)
nc -lvnp 80                                             # raw
```

## Which IP do I give the target?
| Setup | Address |
|---|---|
| Lab (VPN) | your VPN interface IP (`ip a` / `ipconfig`) |
| Local docker (Linux) | bridge gateway: `docker network inspect bridge -f '{{(index .IPAM.Config 0).Gateway}}'` (e.g. `172.17.0.1`), or the compose network gateway |
| Local docker (Win/Mac Docker Desktop) | `host.docker.internal` |
| Podman | `podman network inspect podman` gateway (e.g. `10.88.0.1`) / `host.containers.internal` |
| Target can't reach you | in-container listener or write output to a readable place ([cmdi-blind-oob](../05-injection/cmdi-blind-oob.md)) |

## Public catchers (internet-reachable targets only)
interactsh (`interactsh-client` → gives `xxxx.oast.fun`, logs DNS+HTTP), webhook.site,
requestbin, Burp Collaborator (Pro). DNS callbacks work when HTTP egress is blocked.
